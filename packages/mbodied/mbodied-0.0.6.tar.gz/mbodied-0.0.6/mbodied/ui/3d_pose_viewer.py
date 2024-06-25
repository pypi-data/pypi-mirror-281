import base64
import io
import logging
from io import BytesIO
from pathlib import Path
from time import time

import cv2
import datasets
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
import requests
import torch
from PIL import Image as PILModule
from PIL.Image import Image
from transformers import pipeline

from mbodied.agents.sense.yolo import get_objects
from mbodied.base.agent import Agent

device = "cuda:3" if torch.cuda.is_available() else "cpu"


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils


# Define model_kwargs for Depth Estimation Pipeline
model_kwargs = {
    "device_map": "cuda:3",
    "attn_implementation": "flash_attention_2",
}

# Initialize depth estimation pipelines

ds3 = pipeline(task="depth-estimation", model="LiheYoung/depth-anything-small-hf", **model_kwargs)
ds4 = pipeline(task="depth-estimation", model="nielsr/depth-anything-small", **model_kwargs)
dss = {
    "neilsr": ds4,
    # "neilsr-large": ds5,
    # "young-large": ds6,
    "young-small": ds3,
}

object_detector = Agent(remote_server_name="https://api.mbodi.ai", device=device)


def get_categories(image, task):
    return object_detector.remote_act(dict(image=image, task=task), "phi3v-spatial", blocking=True).result


def get_dataset(
    dataset_path: str = "jxu124/OpenX-Embodiment",
    dataset_name: str = "utokyo_xarm_pick_and_place_converted_externally_to_rlds",
    split: str = "train",
    streaming: bool = True,
    trust_remote_code: bool = True,
):
    logging.info(f"Fetching dataset {dataset_path}/{dataset_name}")
    return datasets.load_dataset(
        dataset_path,
        dataset_name,
        streaming=streaming,
        split=split,
        cache_dir="dataset_cache",
        trust_remote_code=trust_remote_code,
    )


def draw_pose(frame: np.ndarray):
    """Draws pose annotations on a frame and returns pose landmarks.

    Args:
        frame (np.ndarray): The input frame.

    Returns:
        results.pose_landmarks: The pose landmarks.
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    return results.pose_landmarks


def save_depth_image_with_scale(depth, output_path, pose) -> None:
    """Saves a depth image with a color scale and inpaints a pose based on the given parameters.

    Args:
        depth (np.ndarray): The depth image.
        output_path (str): The path to save the depth image with scale.
        xyzrpy (list): A list containing x, y, z, roll, pitch, yaw.
    """
    # Ensure depth is a 2D array
    if len(depth.shape) == 3:
        depth = depth[:, :, 0]

    # Extract pose parameters
    x, y, z, roll, pitch, yaw, grasp = pose

    # Convert milimeters to meters
    # x = x / 1000
    # y = y / 1000
    # z = z / 1000

    # Convert degrees to radians
    # roll = roll * np.pi / 180
    # pitch = pitch * np.pi / 180
    # yaw = yaw * np.pi / 180

    # Create a figure and axis
    fig, ax = plt.subplots()
    ax.set_title(
        f"HandControl: x={x:.2f}, y={y:.2f}, z={z:.2f}, roll={roll:.2f}, pitch={pitch:.2f}, yaw={yaw:.2f}, grasp={grasp}"
    )
    ax.imshow(depth, cmap="inferno")
    plt.colorbar(ax.imshow(depth, cmap="inferno"), ax=ax)

    # Save the figure
    plt.savefig(output_path)
    plt.close()


def apply_sharpening_filter(image: np.ndarray) -> np.ndarray:
    """Apply a sharpening filter to the input image.

    Args:
        image (np.ndarray): The input image to be sharpened.

    Returns:
        np.ndarray: The sharpened image.
    """
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(np.array(image), -1, kernel)


def process_depth_map(predicted_depth, model_name, image_id):
    """Processes and saves the depth map and applies colormap.

    Args:
        predicted_depth (torch.Tensor): The predicted depth tensor.
        model_name (str): Name of the model used.
        image_id (int): ID of the image.
    """
    h, w = predicted_depth.shape[-2:]
    depth = torch.nn.functional.interpolate(predicted_depth[None], (h, w), mode="bilinear", align_corners=False)[0, 0]
    # Normalize depth for colormap
    depth = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
    depth = depth.cpu().numpy().astype(np.uint8)
    # Apply colormap
    colored_depth = cv2.applyColorMap(depth, cv2.COLORMAP_INFERNO)[:, :, ::-1]
    # Save colored depth map
    colored_depth_img = Image.fromarray(colored_depth)
    return apply_sharpening_filter(colored_depth_img)


def main() -> None:
    """Main function to process the dataset and apply depth estimation and pose detection."""
    ds = get_dataset().take(20)

    with torch.no_grad():
        for i, d in enumerate(ds):
            state_accum = np.array(d["data.pickle"]["steps"][0]["observation"]["end_effector_pose"])
            for j, step in enumerate(d["data.pickle"]["steps"]):
                im = step["observation"]["image"]
                img = Image.open(io.BytesIO(im["bytes"]))
                img_output_path = f"outs/image_outs/{i}/{j}.png"
                Path(img_output_path).parent.mkdir(parents=True, exist_ok=True)
                img.save(img_output_path)

                for name, depth_model in dss.items():
                    tic = time()
                    result = depth_model(img_output_path)
                    predicted_depth = result["predicted_depth"]
                    colored_depth_img = process_depth_map(predicted_depth, name, f"{i}_{j}")
                    depth_output_path = f"/data/seb/mbodied_corp/outs/depth_outs/{name}/{i}/{j}.jpeg"

                    pose = step["action"]
                    print(
                        f"action: x:{pose[0]:.2f}, y:{pose[1]:.2f}, z:{pose[2]:.2f}, roll:{pose[3]:.2f}, pitch:{pose[4]:.2f}, yaw:{pose[5]:.2f}"
                    )
                    state = step["observation"]["end_effector_pose"]
                    print(
                        f"state: x:{state[0]:.2f}, y:{state[1]:.2f}, z:{state[2]:.2f}, roll:{state[3]:.2f}, pitch:{state[4]:.2f}, yaw:{state[5]:.2f}"
                    )
                    state_accum += np.array(pose)[:-1]
                    print(
                        f"state_accum: x:{state_accum[0]:.2f}, y:{state_accum[1]:.2f}, z:{state_accum[2]:.2f}, roll:{state_accum[3]:.2f}, pitch:{state_accum[4]:.2f}, yaw:{state_accum[5]:.2f}"
                    )
                    Path(depth_output_path).parent.mkdir(parents=True, exist_ok=True)
                    save_depth_image_with_scale(colored_depth_img, depth_output_path, pose)

                    toc = time()
                    logger.info(f"time for {name}: {toc-tic:.4f} seconds")
                    categories = get_categories(img, step["language_instruction"]).strip().split(",")
                    print(categories)
                    img = get_objects(img, categories)
                    Path(f"outs/object_outs/{name}/{i}/{j}.png").parent.mkdir(parents=True, exist_ok=True)
                    img.save(f"outs/object_outs/{name}/{i}/{j}.png")
                    break
            break


if __name__ == "__main__":
    main()
