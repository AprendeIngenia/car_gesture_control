import math
import cv2
import numpy as np
import mediapipe as mp
from typing import List, Tuple


class HandProcessing:
    def __init__(self, mode=False, hands=1, model_complexity=0, threshold_detection=0.5, threshold_tracking=0.5):
        self.mode = mode
        self.max_hands = hands
        self.complexity = model_complexity
        self.conf_deteccion = threshold_detection
        self.conf_tracking = threshold_tracking

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.complexity, self.conf_deteccion, self.conf_tracking)
        self.draw = mp.solutions.drawing_utils
        self.tip = [4, 8, 12, 16, 20]

    def find_hands(self, frame: np.ndarray, draw: bool = True) -> np.ndarray:
        img_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_color)

        if self.results.multi_hand_landmarks:
            for mano in self.results.multi_hand_landmarks:
                if draw:
                    self.draw.draw_landmarks(frame, mano, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def find_position(self, frame: np.ndarray, hand: int = 0, draw_points: bool = True, draw_box: bool = True, color: List[int] = []) \
            -> Tuple[List[List[int]], Tuple[int, int, int, int]]:
        xlist: List[int] = []
        ylist: List[int] = []
        bbox: Tuple[int, int, int, int] = ()
        hands_list: List[List[int]] = []

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand]
            for id, lm in enumerate(my_hand.landmark):
                alto, ancho, c = frame.shape
                cx, cy = int(lm.x * ancho), int(lm.y * alto)
                xlist.append(cx)
                ylist.append(cy)
                hands_list.append([id, cx, cy])
                if draw_points:
                    cv2.circle(frame, (cx, cy), 3, (0, 0, 0), cv2.FILLED)

            xmin, xmax = min(xlist), max(xlist)
            ymin, ymax = min(ylist), max(ylist)
            bbox = xmin, ymin, xmax, ymax
            if draw_box:
                cv2.rectangle(frame, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), color, 2)
        return hands_list, bbox

    def fingers_up(self, keypoints_list: List[List[int]]) -> List[int]:
        fingers: List[int] = []
        if keypoints_list[self.tip[0]][1] > keypoints_list[self.tip[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for i in range(1, 5):
            if keypoints_list[self.tip[i]][2] < keypoints_list[self.tip[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def distance(self, p1: int, p2: int, frame: np.ndarray, draw: bool = True, radio: int = 15, thickness: int = 3) -> \
            Tuple[float, np.ndarray, list]:
        x1, y1 = self.list[p1][1:]
        x2, y2 = self.list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), thickness)
            cv2.circle(frame, (x1, y1), radio, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), radio, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (cx, cy), radio, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, frame, [x1, y1, x2, y2, cx, cy]
