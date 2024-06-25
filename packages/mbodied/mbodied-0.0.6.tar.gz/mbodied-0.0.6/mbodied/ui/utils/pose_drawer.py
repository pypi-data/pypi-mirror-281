import cv2
from matplotlib import pyplot as plt
from cv2 import aruco
import numpy as np
from mbodied.types.utils.geometry import rpy_to_rotation_matrix

CAMERA_MATRIX = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
DISTORITION = np.zeros((5, 1))


def draw_pose(self, image, pose, camera_matrix=CAMERA_MATRIX, distorsion_coefficients=DISTORITION):
    """Visualizes the detected markers and their poses on the given frame.

    Args:
      image: The frame to draw the poses on.
      pose: The pose of the camera.
      objects: A dictionary of objects and their world coordinates.
      camera_matrix: The camera matrix.
    """
    rotation_matrix = rpy_to_rotation_matrix(pose[3:])
    translation = np.array(pose[:3])
    image = cv2.drawFrameAxes(image, camera_matrix, distorsion_coefficients, rotation_matrix, translation, 0.1)

    plt.figure()
    plt.imshow(image)
    plt.grid()
    plt.show()
    plt.figure().savefig("output.png")
