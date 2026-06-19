import cv2
from hand_tracker import HandTracker
import pyautogui
import math
import time

cap = cv2.VideoCapture(0)

tracker = HandTracker()

screen_w, screen_h = pyautogui.size()

last_click_time = 0
last_right_click_time = 0
last_scroll_time = 0
last_double_click_time = 0

prev_x = 0
prev_y = 0

smoothening = 5

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame, x, y, thumb_x, thumb_y, middle_x, middle_y, ring_x, ring_y = tracker.detect(frame)

    if x is not None:

        cam_w = frame.shape[1]
        cam_h = frame.shape[0]

        screen_x = int((x / cam_w) * screen_w)
        screen_y = int((y / cam_h) * screen_h)

        curr_x = prev_x + (screen_x - prev_x) / smoothening
        curr_y = prev_y + (screen_y - prev_y) / smoothening

        pyautogui.moveTo(curr_x, curr_y)

        prev_x = curr_x
        prev_y = curr_y

        # LEFT CLICK (Thumb + Index)
        if thumb_x is not None:

            distance = math.hypot(
                thumb_x - x,
                thumb_y - y
            )

            if distance < 40:

                current_time = time.time()

                if current_time - last_click_time > 1:

                    pyautogui.click()

                    last_click_time = current_time

                    cv2.putText(
                        frame,
                        "LEFT CLICK",
                        (200, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

        # RIGHT CLICK (Index + Middle)
        if middle_x is not None:

            right_distance = math.hypot(
                middle_x - x,
                middle_y - y
            )

            if right_distance < 35:

                current_time = time.time()

                if current_time - last_right_click_time > 1:

                    pyautogui.rightClick()

                    last_right_click_time = current_time

                    cv2.putText(
                        frame,
                        "RIGHT CLICK",
                        (200, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        3
                    )

        # SCROLL FEATURE
        if middle_y is not None:

            current_time = time.time()

            if current_time - last_scroll_time > 0.5:

                if middle_y < y - 40:

                    pyautogui.scroll(100)

                    cv2.putText(
                        frame,
                        "SCROLL UP",
                        (200, 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 255),
                        3
                    )

                    last_scroll_time = current_time

                elif middle_y > y + 40:

                    pyautogui.scroll(-100)

                    cv2.putText(
                        frame,
                        "SCROLL DOWN",
                        (200, 150),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 255),
                        3
                    )

                    last_scroll_time = current_time

        # DOUBLE CLICK (Thumb + Ring)
        if ring_x is not None and thumb_x is not None:

            ring_distance = math.hypot(
                ring_x - thumb_x,
                ring_y - thumb_y
            )

            if ring_distance < 35:

                current_time = time.time()

                if current_time - last_double_click_time > 1:

                    pyautogui.doubleClick()

                    last_double_click_time = current_time

                    cv2.putText(
                        frame,
                        "DOUBLE CLICK",
                        (200, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 0),
                        3
                    )

        cv2.putText(
            frame,
            f"X:{x} Y:{y}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("Hand Detection", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()