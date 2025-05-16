import mediapipe as mp
mp_hands = mp.solutions.hands

def hello(hand_landmarks):
    # hand open
    if hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y:
        # thumb extended
        if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y:
            # finger extended
            if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y:
                return True
    return False