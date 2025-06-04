import cv2
import time
import numpy as np
import mediapipe as mp
from helpers.lgp_recognition import LGPRecognition
from helpers.lgp_gesture_creator import LGPGestureCreator

#######################################
# SPLASH SCREEN PEQUENA PARA A CAMARA #
#######################################
loading = np.zeros((640, 640, 3), dtype=np.uint8)
cv2.putText(loading, "LGP Sentence Composition", (40, 320), cv2.FONT_HERSHEY_TRIPLEX, 1.2, (255, 255, 255), 3, cv2.LINE_AA)
cv2.putText(loading, "A iniciar camara...", (200, 400), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (200, 200, 200), 2, cv2.LINE_AA)

start = time.time()

while time.time() - start < 1.5:
    cv2.imshow("A carregar...", loading)
    cv2.waitKey(1)

cv2.destroyWindow("A carregar...")

##############################
# INICIO DA DETEÇÃO DAS MÃOS #
##############################
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.5)

recognizer = LGPRecognition()
gesture_creator = LGPGestureCreator()
last_gesture = None
last_gesture_time = 0
line_break_added = False
gesture_start_time = 0
sentence = ""

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

def draw_text(img, text, pos, font, scale, color, thickness, line_height=35):
    lines = text.split('\n')
    x, y = pos
    for i, line in enumerate(lines):
        y_offset = y + i * line_height
        cv2.putText(img, line, (x, y_offset), font, scale, color, thickness)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    current_time = time.time()
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
            
            gesture = recognizer.recognize(hand_landmarks)
            
            if gesture:
                cv2.putText(frame, f'Gesto atual: {gesture}', (10, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                if gesture != last_gesture:
                    last_gesture = gesture
                    gesture_start_time = current_time
                elif current_time - gesture_start_time >= 1.0:
                    sentence = recognizer.add_gesture_to_sentence(gesture, sentence)
                    last_gesture_time = current_time
                    line_break_added = False
                    last_gesture = None 
            else:
                last_gesture = None
                gesture_start_time = 0
            
        
    if last_gesture_time:
        time_since_last_gesture = current_time - last_gesture_time
        countdown = max(0, 8 - int(time_since_last_gesture))
        cv2.putText(frame, f'Tempo restante para trocar de linha: {countdown}s', (10, 135), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if last_gesture_time and (time.time() - last_gesture_time >= 8) and not line_break_added:
        sentence += "\n"
        line_break_added = True

    draw_text(frame, f'Frase: {sentence}', (10, frame.shape[0] - 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.rectangle(frame, (10, 10), (360, 60), (0, 0, 255), -1)
    cv2.putText(frame, 'Criar gesto personalizado (C)', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imshow('LGP - Sentence Composition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('c'):
        gesture_creator.open_gesture_creator_ui()
        recognizer.update_gestures()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()