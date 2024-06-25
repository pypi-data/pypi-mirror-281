import pytest
from unittest.mock import MagicMock, patch
import numpy as np
from mbodied.hri.hri_xarm import HRIInterface
import signal


@pytest.fixture
def hri_interface():
    with (
        patch("mbodied.agents.sense.object_pose_estimator_3d.ObjectPoseEstimator3D.__init__", lambda x: None),
        patch("mbodied.hardware.xarm_interface.XarmInterface.__init__", lambda x: None),
        patch("mbodied.agents.language.LanguageAgent.__init__", lambda x, context, model_src: None),
        patch("mbodied.agents.sense.audio.audio_handler.AudioHandler.__init__", lambda x: None),
        patch("wandb.init", return_value=None),
        patch("os.environ", {}),
    ):
        interface = HRIInterface(backend="openai", debug=True, enable_audio=False)
        interface.object_pose_estimation_client = MagicMock()
        interface.robotic_arm = MagicMock()
        interface.language_router = MagicMock(model_src="openai")
        interface.audio_handler = MagicMock()

        return interface


def test_initialization(hri_interface):
    assert hri_interface.language_router.model_src == "openai"
    assert hri_interface.debug is True
    assert hri_interface.enable_audio is False
    assert hri_interface.xyz_delta == [0, 0, 0]
    assert np.array_equal(hri_interface.xarm_end_effector_pose, np.array([0.3, 0.0, 0.15]))
    assert hri_interface.depth_pickup == 0.0
    assert hri_interface.depth_drop == 0.1
    assert hri_interface.stop_signal_received.is_set() is False


def test_extract_object_poses(hri_interface):
    object_pose_data = np.array(
        [{"data": [{"Basket": [0.1, 0.1, 0.1], "Black Tray": [0.2, 0.2, 0.2], "Object": [0.3, 0.3, 0.3]}]}]
    )
    end_effector_pose = np.array([0.0, 0.0, 0.0])
    depth_pickup = 0.1
    depth_drop = 0.2

    updated_poses = hri_interface.extract_object_poses(object_pose_data, end_effector_pose, depth_pickup, depth_drop)

    assert np.isclose(updated_poses["Basket"][2], depth_drop).all()
    assert np.isclose(updated_poses["Black Tray"][2], depth_drop).all()
    assert np.isclose(updated_poses["Object"][2], depth_pickup).all()


def test_signal_handler(hri_interface):
    with patch("threading.Event.set", autospec=True) as MockEventSet:
        hri_interface.signal_handler(signal.SIGINT, None)
        MockEventSet.assert_called_once()


if __name__ == "__main__":
    pytest.main()
