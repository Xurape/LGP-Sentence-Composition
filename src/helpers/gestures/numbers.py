import mediapipe as mp
mp_hands = mp.solutions.hands

def one(hand_landmarks):
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y:
            return False
        
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP] 
    middle_finger_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    if abs(thumb_tip.x - middle_finger_pip.x) > 0.05 or abs(thumb_tip.y - middle_finger_pip.y) > 0.05:
        return False
        
    return True