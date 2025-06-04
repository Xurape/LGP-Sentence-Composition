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

# EU -> Dedo na horizontal e outros dedos não se vêm
def be_horizontal(hand_landmarks):
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    
    if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < 0.5:
        return False
    
    for i in range(len(finger_tips)):
        if i == 1:  
            continue
        
        if hand_landmarks.landmark[finger_tips[i]].visibility > 0.5:
            return False
    
    return True

# QUERO -> Mão aberta e polegar para cima
def be_open_horizontal(hand_landmarks):
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    
    if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < 0.5:
        return False
    
    for i in range(len(finger_tips)):
        if i == 1:  
            continue
        
        if hand_landmarks.landmark[finger_tips[i]].visibility < 0.5:
            return False
    
    return True

# JOGAR -> quatro dedos estão juntos a apontar para baixo e o polegar não está visível
def be_fingers_down(hand_landmarks):
    finger_tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].visibility < 0.5:
            return False
    
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].visibility > 0.5:
        return False
    
    return True
