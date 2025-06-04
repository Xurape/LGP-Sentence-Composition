import cv2
import mediapipe as mp
import json
import math

class LGPGestureCreator:
    def __init__(self):
        self.gestures = {}
        
    def extract_distances(self, hand_landmarks):
        tips = [4, 8, 12, 16, 20] 
        distances = {}
        
        for i in range(len(tips)):
            for j in range(i+1, len(tips)):
                lm1 = hand_landmarks.landmark[tips[i]]
                lm2 = hand_landmarks.landmark[tips[j]]
                
                #? determinar a distância euclidinada entre todos os pontos
                #? formula -> √((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2) 
                
                dist = ((lm1.x - lm2.x) ** 2 + (lm1.y - lm2.y) ** 2 + (lm1.z - lm2.z) ** 2) ** 0.5
                distances[f"{tips[i]}_{tips[j]}"] = dist
                
        return distances

    def save_gesture(self, gesture_name, hand_landmarks):
        extracted_distances = self.extract_distances(hand_landmarks)
        
        data = {
            "name": gesture_name,
            "distances": extracted_distances
        }
        
        with open(f"helpers/gestures/custom/{gesture_name}.json", "w") as f:
            json.dump(data, f)
            
    def load_gesture(self, gesture_name):
        with open(f"helpers/gestures/custom/{gesture_name}.json") as f:
            return json.load(f)

    def match_gesture(self, hand_landmarks, gesture_data, threshold=0.05):
        distances = self.extract_distances(hand_landmarks)
        
        for key, value in gesture_data["distances"].items():
            if key not in distances or abs(distances[key] - value) > threshold:
                return False
            
        return True
    
    def open_gesture_creator_ui(self):
        print("[DEBUG] A abrir criador de gestos...")
        
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
        mp_drawing = mp.solutions.drawing_utils
        gesture_name = ""
        is_recording = False
        
        #! fix ao circular import
        from helpers.lgp_recognition import LGPRecognition 
        recognizer = LGPRecognition()
        
        print("[DEBUG] Criador de gestos aberto.")
        
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            
            if is_recording:
                cv2.putText(frame, "Modo gravacao ligado - [Pressionar S para guardar]", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.putText(frame, "R - Gravar novo gesto", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "S - Guardar gesto", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "G - Sair", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            
            fingertip_indices = [
                mp_hands.HandLandmark.THUMB_TIP,
                mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP,
            ]
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    for i, index in enumerate(fingertip_indices):
                        fingertip = hand_landmarks.landmark[index]
                        cv2.putText(frame, f'{index.name}: ({fingertip.x:.2f}, {fingertip.y:.2f})', (10, 170 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        
                gesture = recognizer.recognize(hand_landmarks)
            
                if gesture:
                    cv2.putText(frame, f'Gesto atual: {gesture}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                        
            cv2.imshow("Criador de gestos", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('r'):
                is_recording = True
                gesture_name = input("[INPUT] Nome do gesto: ")
            elif key == ord('s'):
                if is_recording and gesture_name:
                    is_recording = False
                    cv2.putText(frame, f"Gesto '{gesture_name}' guardado!", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    self.save_gesture(gesture_name, results.multi_hand_landmarks[0])
                    self.gestures[gesture_name] = self.load_gesture(gesture_name)
                    print(f"[DEBUG] Gesto '{gesture_name}' guardado com sucesso.")
                    print(self.gestures)
            elif key == ord('g'):
                break
            elif key == 27:
                break
            
        hands.close()
        cap.release()
        cv2.destroyAllWindows()
        
        print("[DEBUG] Criador de gestos fechado.")
        return self.gestures
        