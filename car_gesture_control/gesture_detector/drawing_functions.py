import cv2
import numpy as np


class DrawingFunctions:
    def __init__(self):
        self.img_forward = cv2.imread('gesture_detector/resources/images/forward.png')
        self.img_reverse = cv2.imread('gesture_detector/resources/images/reverse.png')
        self.img_left = cv2.imread('gesture_detector/resources/images/left.png')
        self.img_right = cv2.imread('gesture_detector/resources/images/right.png')
        self.img_stop = cv2.imread('gesture_detector/resources/images/stop.png')

    def draw_image(self, original_frame: np.ndarray, action_image: np.ndarray):
        al, an, c = action_image.shape
        original_frame[600:600 + al, 50:50 + an] = action_image
        return original_frame

    def draw_actions(self, action: str, original_frame: np.ndarray) -> np.ndarray:

        actions_dict = {
            'A': self.img_forward,
            'P': self.img_stop,
            'I': self.img_left,
            'D': self.img_right,
            'R': self.img_reverse,
        }
        if action in actions_dict:
            movement_image = actions_dict[action]
            original_frame = self.draw_image(original_frame, movement_image)
        return original_frame