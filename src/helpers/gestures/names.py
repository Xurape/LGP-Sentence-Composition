import mediapipe as mp
mp_hands = mp.solutions.hands

# JOGO -> duas mãos a visíveis e nessas mãos quatro dedos estão juntos a apontar para baixo e o polegar não está visível
def both_hands_fingers_down(hand_landmarks):
    if len(hand_landmarks) != 2:
        return False
    
    for hand in hand_landmarks:
        finger_tips = [
            mp_hands.HandLandmark.INDEX_FINGER_TIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            mp_hands.HandLandmark.RING_FINGER_TIP,
            mp_hands.HandLandmark.PINKY_TIP
        ]
        
        for tip in finger_tips:
            if hand.landmark[tip].visibility < 0.5:
                return False
        
        if hand.landmark[mp_hands.HandLandmark.THUMB_TIP].visibility > 0.5:
            return False
    
    return True