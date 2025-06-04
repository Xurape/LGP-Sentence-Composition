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

def want(hand_landmarks):
    fingers = [
        (mp.solutions.hands.HandLandmark.THUMB_TIP, mp.solutions.hands.HandLandmark.THUMB_IP),
        (mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP, mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP),
        (mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP, mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP),
        (mp.solutions.hands.HandLandmark.RING_FINGER_TIP, mp.solutions.hands.HandLandmark.RING_FINGER_PIP),
        (mp.solutions.hands.HandLandmark.PINKY_TIP, mp.solutions.hands.HandLandmark.PINKY_PIP),
    ]

    for tip, pip in fingers:
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y:
            return False

    fingertip_indices = [
        mp.solutions.hands.HandLandmark.THUMB_TIP,
        mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP,
        mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp.solutions.hands.HandLandmark.RING_FINGER_TIP,
        mp.solutions.hands.HandLandmark.PINKY_TIP,
    ]

    for i in range(len(fingertip_indices) - 1):
        current_tip_x = hand_landmarks.landmark[fingertip_indices[i]].x
        next_tip_x = hand_landmarks.landmark[fingertip_indices[i + 1]].x

        if next_tip_x > current_tip_x - 0.02:
            return False

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