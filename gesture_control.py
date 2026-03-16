import cv2
import mediapipe as mp
import numpy as np


class GestureController:

    def __init__(self):

        # Webcam
        self.cap = cv2.VideoCapture(0)

        # Mediapipe hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils

        # Gesture values
        self.x_movement = 0
        self.y_movement = 0
        self.zoom = 0

        # Hand detection flag
        self.hand_detected = False


    def update(self):

        ret, frame = self.cap.read()

        if not ret:
            return

        frame = cv2.flip(frame,1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        self.hand_detected = False

        if results.multi_hand_landmarks:

            self.hand_detected = True

            for hand in results.multi_hand_landmarks:

                index_tip = hand.landmark[8]
                thumb_tip = hand.landmark[4]

                # movement
                self.x_movement = index_tip.x
                self.y_movement = index_tip.y

                # pinch distance for zoom
                distance = np.sqrt(
                    (index_tip.x - thumb_tip.x)**2 +
                    (index_tip.y - thumb_tip.y)**2
                )

                self.zoom = distance

                self.mp_draw.draw_landmarks(
                    frame,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("Gesture Control", frame)
        cv2.waitKey(1)


    # rotation values
    def get_rotation(self):

        rot_x = (self.y_movement - 0.5) * 200
        rot_y = (self.x_movement - 0.5) * 200

        return rot_x, rot_y


    # zoom value
    def get_zoom(self):

        return -20 + self.zoom * 40


    # hand detection check
    def is_hand_detected(self):

        return self.hand_detected