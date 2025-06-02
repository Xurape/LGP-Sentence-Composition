import cv2
import time
import mediapipe as mp
from helpers.lgp_recognition import LGPRecognition


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.5)

recognizer = LGPRecognition()
last_gesture = None
gesture_start_time = 0
sentence = ""

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
            )
            
            cv2.putText(frame, 'Mao detectada', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            fingertip_indices = [
                mp_hands.HandLandmark.THUMB_TIP,
                mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP,
            ]

            for i, index in enumerate(fingertip_indices):
                fingertip = hand_landmarks.landmark[index]
                cv2.putText(frame, f'{index.name}: ({fingertip.x:.2f}, {fingertip.y:.2f})', (10, 90 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            gesture = recognizer.recognize(hand_landmarks)
            
            current_time = time.time()
            if gesture:
                cv2.putText(frame, f'Gesto atual: {gesture}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                if gesture != last_gesture:
                    last_gesture = gesture
                    gesture_start_time = current_time
                elif current_time - gesture_start_time >= 1.0:
                    if gesture == "Ola":
                        sentence += gesture + ", "
                    else:
                        sentence += gesture + " "
                    last_gesture = None 
            else:
                last_gesture = None
                gesture_start_time = 0

    cv2.putText(frame, f'Frase: {sentence}', (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.imshow('LGP - Sentence Composition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()