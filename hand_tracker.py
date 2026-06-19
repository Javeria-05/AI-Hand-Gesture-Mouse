import cv2
import mediapipe as mp

class HandTracker:

    def __init__(self):
        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.draw = mp.solutions.drawing_utils

    def detect(self, frame):

        h, w, c = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        index_x = None
        index_y = None

        thumb_x = None
        thumb_y = None

        middle_x = None
        middle_y = None

        ring_x = None
        ring_y = None

        if results.multi_hand_landmarks:

            for hand in results.multi_hand_landmarks:

                self.draw.draw_landmarks(
                    frame,
                    hand,
                    self.mpHands.HAND_CONNECTIONS
                )

                index_tip = hand.landmark[8]
                thumb_tip = hand.landmark[4]
                middle_tip = hand.landmark[12]
                ring_tip = hand.landmark[16]

                index_x = int(index_tip.x * w)
                index_y = int(index_tip.y * h)

                thumb_x = int(thumb_tip.x * w)
                thumb_y = int(thumb_tip.y * h)

                middle_x = int(middle_tip.x * w)
                middle_y = int(middle_tip.y * h)

                ring_x = int(ring_tip.x * w)
                ring_y = int(ring_tip.y * h)

                cv2.circle(frame, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 0), cv2.FILLED)

        return frame, index_x, index_y, thumb_x, thumb_y, middle_x, middle_y, ring_x, ring_y