import mediapipe as mp
mp_hands = mp.solutions.hands

def hello(hand_landmarks):
    fingers = [
        (mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_IP),
        (mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP),
        (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
        (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
        (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP),
    ]
    
    for tip, pip in fingers:
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y:
            return False

    fingertip_indices = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP,
    ]
    
    for i in range(len(fingertip_indices) - 1):
        tip1 = hand_landmarks.landmark[fingertip_indices[i]]
        tip2 = hand_landmarks.landmark[fingertip_indices[i + 1]]
        
        distance = ((tip1.x - tip2.x) ** 2 + (tip1.y - tip2.y) ** 2) ** 0.5
        
        if i == 0:
            if distance < 0.10:
                return False
        else:
            if distance < 0.04:
                return False

    return True


def goodbye(hand_landmarks):
    fingers = [
        (mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_IP),
        (mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP),
        (mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
        (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
        (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP),
    ]
    
    for tip, pip in fingers:
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y:
            return False

    fingertip_indices = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP,
    ]
    
    for i in range(len(fingertip_indices) - 1):
        tip1 = hand_landmarks.landmark[fingertip_indices[i]]
        tip2 = hand_landmarks.landmark[fingertip_indices[i + 1]]
        
        #? formula -> √((x1 - x2)^2 + (y1 - y2)^2)
        distance = ((tip1.x - tip2.x) ** 2 + (tip1.y - tip2.y) ** 2) ** 0.5
        
        if i == 0:
            if distance > 0.15:
                return False
        else:
            if distance > 0.06:
                return False

    return True