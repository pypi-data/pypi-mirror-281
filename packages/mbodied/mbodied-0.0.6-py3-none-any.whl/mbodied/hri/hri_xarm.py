import contextlib
import json
import logging
import os
import threading
import signal

import click
from filelock import FileLock
import numpy as np
import wandb

from mbodied.hardware.xarm_interface import XarmInterface
from mbodied.agents.language import LanguageAgent
from mbodied.agents.sense.audio.audio_handler import AudioHandler
from mbodied.types.motion_controls import HandControl, JointControl, Pose
from mbodied.types.sense.vision import Image
from mbodied.agents.sense.object_pose_estimator_3d import ObjectPoseEstimator3D

SYSTEM_PROMPT = """You are a robot with vision capabilities. You have a white arm with a gripper at the end.
        For each task given, you respond with an action or answer in the form of the following json object:
        {
            "robotreply": "Your textual response here.",
            "actions": [{'x':, 'y':, 'z':, 'roll':, 'pitch':, 'yaw':, 'grasp':}, ...],
            "finished": true or false
        }
        - you can output a list of actions if you think it's necessary. return empty list for actions if there's no action to take or if I'm just chatting with you.
        Some note about the action values:
        All these values are end effector delta.
        - x, y, z: The x, y, z in meters of the robot's hand (gripper) movement. +x means forward, -x means backward, +y means left, -y means right.
        - roll, pitch, yaw: The roll, pitch, yaw angle of the robot's hand (gripper).
        - grasp: The grasp value of the robot's hand (gripper). 0 is close 1 is open.
        For example,
        if you want to move your hand (gripper) forward, x should be values i.e. 0.1.
        if you want to move your hand (gripper) backward, x should be values i.e. -0.1.
        if you want to move your hand (gripper) right a lot, x should be -0.2, etc.

        You must refer to the object location before outputting actions.

        You are about 0.15 meters away on Z coordinate from the table to pick something from your very initial position.
        Here's just an example picking something up from the table to the right of you from your initial position:
        [{'x': 0, 'y': -0.2, 'z': 0, 'roll': 0, 'pitch': 0, 'yaw': 0, 'grasp': 1},
        {'x': 0, 'y': 0, 'z': -0.15, 'roll': 0, 'pitch': 0, 'yaw': 0, 'grasp': 1},
        {'x': 0, 'y': 0, 'z': 0, 'roll': 0, 'pitch': 0, 'yaw': 0, 'grasp': 0},
        {'x': 0, 'y': 0, 'z': 0.15, 'roll': 0, 'pitch': 0, 'yaw': 0, 'grasp': 0}]
        Remember to evaluate where things are in real time to output the exact action values.

        And to place something down, you need to go down first and then open the gripper and go up.
        """


class HRIInterface:
    """Human-Robot Interaction Interface for controlling robotic arm using language instructions."""

    def __init__(self, backend: str, debug: bool, enable_audio: bool) -> None:
        """Initialize HRIInterface with the specified parameters.

        Args:
            backend (str): The backend service for language processing.
            debug (bool): Flag to enable or disable debug logging.
            enable_audio (bool): Flag to enable or disable audio input/output.
        """
        self.object_pose_estimation_agent = ObjectPoseEstimator3D()
        self.robotic_arm = XarmInterface()
        self.audio_handler = AudioHandler()
        self.language_agent = LanguageAgent(context=SYSTEM_PROMPT, model_src=backend)
        self.enable_audio = enable_audio
        self.debug = debug
        self.xyz_delta = [0, 0, 0]
        self.xarm_end_effector_pose = np.array([0.3, 0.0, 0.15])
        self.depth_pickup = 0.0
        self.depth_drop = 0.1

        self.stop_signal_received = threading.Event()

        if self.debug:
            logging.basicConfig(level=logging.DEBUG, force=True)

        signal.signal(signal.SIGINT, self.signal_handler)

        wandb.init(project="xarm-hri-experiment")

        os.environ["OPENAI_API_KEY"] = "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"
        os.environ["ANTHROPIC_API_KEY"] = (
            "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"
        )

    def extract_object_poses(
        self, object_pose_data: np.ndarray, end_effector_pose: np.ndarray, depth_pickup: float, depth_drop: float
    ) -> dict:
        """Extract object poses from the given data.

        Args:
            object_pose_data (np.ndarray): The raw pose data of objects.
            end_effector_pose (np.ndarray): The pose of the robotic arm's end effector.
            depth_pickup (float): Depth value for picking up objects.
            depth_drop (float): Depth value for dropping objects.

        Returns:
            dict: A dictionary of object names and their corresponding poses.

        Example:
            >>> object_pose_data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            >>> end_effector_pose = np.array([1, 1, 1])
            >>> hri = HRIInterface("openai", False, False)
            >>> hri.extract_object_poses(object_pose_data, end_effector_pose, 0.0, 0.1)
            {'Object': np.array([[0, 0, 0]])}
        """
        object_pose_data_dict = object_pose_data.item()
        object_data = object_pose_data_dict["data"]

        updated_object_poses = {}

        object_poses = object_data[0]

        for name, pose in object_poses.items():
            pose = np.array(pose).reshape(3, 1)

            if name == "Basket" or name == "Black Tray":
                pose[2] = depth_drop
            else:
                pose[2] = depth_pickup

            pose = pose - end_effector_pose.reshape(3, 1)
            pose = np.round(pose, 3)
            updated_object_poses[name] = pose

        return updated_object_poses

    def parse_actions_json(self, json_data: dict) -> list:
        """Parse actions from JSON data and create a list of HandControl objects.

        Args:
            json_data (dict): JSON data containing actions.

        Returns:
            list: A list of HandControl objects.

        Example:
            >>> json_data = {"actions": [{"x": 0.1, "y": 0.2, "z": 0.3, "roll": 0.0, "pitch": 0.0, "yaw": 0.0, "grasp": 1}]}
            >>> hri = HRIInterface("openai", False, False)
            >>> hri.parse_actions_json(json_data)
            [HandControl(pose=Pose(xyz=[0.1, 0.2, 0.3], rpy=[0.0, 0.0, 0.0]), grasp=JointControl(value=1))]
        """
        hand_control_list = []
        for action in json_data["actions"]:
            self.xyz_delta[0] += action.get("x", 0)
            self.xyz_delta[1] += action.get("y", 0)
            self.xyz_delta[2] += action.get("z", 0)
            hand_control_list.append(
                HandControl(
                    pose=Pose(
                        xyz=[action.get("x", 0), action.get("y", 0), action.get("z", 0)],
                        rpy=[action.get("roll", 0), action.get("pitch", 0), action.get("yaw", 0)],
                    ),
                    grasp=JointControl(value=action.get("grasp", 0)),
                )
            )
        return hand_control_list

    def hri_interface(self, user_prompt: str) -> str:
        """Handle human-robot interaction based on user prompt.

        Args:
            user_prompt (str): The prompt or instruction from the user.

        Returns:
            str: The robot's textual response.

        Example:
            >>> hri = HRIInterface("openai", False, False)
            >>> hri.hri_interface("move forward")
            "Moving forward"
        """
        if user_prompt == "exit":
            wandb.finish()
            return

        with FileLock("object_poses.npy.lock"):
            data = np.load("object_poses.npy", allow_pickle=True)

        new_object_poses = self.extract_object_poses(
            data, self.xarm_end_effector_pose, self.depth_pickup, self.depth_drop
        )

        file_path = "depth_map.jpg"
        lock = FileLock(file_path + ".lock")
        with lock:
            image = Image(file_path)

        message = "("
        for name, pose in new_object_poses.items():
            message += f"The position of the {name} with respect to the end effector is {pose.flatten().tolist()}. "
        message += f"The X,Y,Z you moved so far: {self.xyz_delta}. Respond in JSON). Current instruction: {user_prompt}"

        response = self.language_agent.act(message, image)[0]
        response = response.replace("```json", "").replace("```", "")
        with contextlib.suppress(json.JSONDecodeError):
            json_data = json.loads(response)

        if self.enable_audio:
            self.audio_handler.speak(json_data["robotreply"])
        hand_control_list = self.parse_actions_json(json_data)
        for hand_control in hand_control_list:
            self.robotic_arm.do(hand_control)

        wandb.log(
            {
                "observation prompt and response": wandb.Image(
                    image.pil, caption=f"prompt {message}, response {response}"
                )
            }
        )

        return json_data["robotreply"], hand_control_list

    def signal_handler(self, signal, frame) -> None:
        """Handle the interrupt signal to stop the program."""
        print("Signal received, stopping...")
        self.stop_signal_received.set()

    def run_pose_estimation(self) -> None:
        """Run the pose estimation loop until a stop signal is received."""
        while not self.stop_signal_received.is_set():
            try:
                response = self.object_pose_estimation_agent.act()
                print(response)
            except Exception as e:
                print(e)


@click.command("hri")
@click.option("--backend", default="openai", help="The backend to use", type=click.Choice(["anthropic", "openai"]))
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option("--n_frames", default=5, help="Number of frames to buffer before processing")
@click.option("--enable_audio", default=True, help="Enable audio input/output")
def main(backend: str, debug: bool, n_frames: int, enable_audio: bool) -> None:
    """Main function to initialize and run the HRI interface."""
    hri_interface = HRIInterface(backend, debug, enable_audio)

    pose_estimation_thread = threading.Thread(target=hri_interface.run_pose_estimation)
    pose_estimation_thread.start()

    try:
        while not hri_interface.stop_signal_received.is_set():
            task = hri_interface.audio_handler.listen() if enable_audio else input("Instruction: ")

            hri_interface.hri_interface(task)

    finally:
        hri_interface.robotic_arm.arm.set_position(*hri_interface.robotic_arm.home_pos, wait=True, speed=300)
        pose_estimation_thread.join()


if __name__ == "__main__":
    main()
