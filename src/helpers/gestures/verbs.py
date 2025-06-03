import mediapipe as mp
mp_hands = mp.solutions.hands

def be(hand_landmarks):
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    
    for i in range(len(finger_tips)):
        if i == 1:  
            continue
        
        distance = abs(hand_landmarks.landmark[finger_tips[i]].x - hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
        
        if distance < 0.1:
            return False
    
    return True
    