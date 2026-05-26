#with opacitied canvas, changeable colors, and lines that are smoother
import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # add these!
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
color = (255, 255, 255)
prev_x, prev_y = None, None

def count_fingers(hand_landmarks, h, w):
    tips = [8, 12, 16, 20]
    count = 0
    for tip in tips:
        tip_y = int(hand_landmarks.landmark[tip].y * h)
        pip_y = int(hand_landmarks.landmark[tip - 2].y * h)
        if tip_y < pip_y:
            count += 1
    return count

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(result.multi_hand_landmarks):
            handedness = result.multi_handedness[i].classification[0].label

            if handedness == "Left":
                fingers = count_fingers(hand_landmarks, h, w)
                if fingers == 1:   color = (0, 0, 255)
                elif fingers == 2: color = (0, 255, 255)
                elif fingers == 3: color = (0, 255, 0)
                elif fingers == 4: color = (255, 0, 0)
                else:              color = (255, 255, 255)

            elif handedness == "Right":
                x   = int(hand_landmarks.landmark[8].x * w)
                y   = int(hand_landmarks.landmark[8].y * h)
                y7  = int(hand_landmarks.landmark[7].y * h)
                y12 = int(hand_landmarks.landmark[12].y * h)
                fingers_right = count_fingers(hand_landmarks, h, w)
                if y < y7:  # finger up → draw
                    if prev_x is not None and prev_y is not None:
                        
                        cv2.line(canvas, (prev_x, prev_y), (x, y), color, 20)
                    prev_x, prev_y = x, y  # always update

                else:  # finger down → reset
                    prev_x, prev_y = None, None
                    if abs(y-y12)<70:  # erase
                        
                        cv2.circle(canvas, (x, y), 30, (0, 0, 0), -1)
                
    blended = cv2.addWeighted(frame, 0.3, canvas, 1, 0)
    cv2.imshow("Air Drawing", blended)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()