import mediapipe as mp
mp_hands = mp.solutions.hands

# UM -> polegar está para cima e os restantes dedos estão juntos e na horizontal
def one(hand_landmarks):
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y:
        return False
    
    finger_tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].visibility < 0.5:
            return False
    
    return True