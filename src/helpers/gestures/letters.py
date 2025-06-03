import mediapipe as mp
mp_hands = mp.solutions.hands


def J(hand_landmarks):
    finger_tips =  [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    
    for i in range(len(finger_tips)):
        if i == 0:
            continue
        
        if hand_landmarks.landmark[finger_tips[i]].y >  hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y:
            return False
        
    for i in range(len(finger_tips) - 1):
        if abs(hand_landmarks.landmark[finger_tips[i]].x - hand_landmarks.landmark[finger_tips[i + 1]].x) > 0.10 and abs(hand_landmarks.landmark[finger_tips[i]].y - hand_landmarks.landmark[finger_tips[i + 1]].y) > 0.10:
            return False
        
    return True

def O(hand_landmarks):
    finger_tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y:
        return False
    
    for i in range(len(finger_tips)):
        if hand_landmarks.landmark[finger_tips[i]].x < (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x - 0.10) or hand_landmarks.landmark[finger_tips[i]].x > (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x + 0.10):
            return False
        
        if hand_landmarks.landmark[finger_tips[i]].y < (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y - 0.05) or hand_landmarks.landmark[finger_tips[i]].y > (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y + 0.05):
            return False
    
    return True

def A(hand_landmarks):
    finger_tips = [
        mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP,
        mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp.solutions.hands.HandLandmark.RING_FINGER_TIP,
        mp.solutions.hands.HandLandmark.PINKY_TIP
    ]
    
    finger_mcp = [ 
        mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP,
        mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP,
        mp.solutions.hands.HandLandmark.RING_FINGER_MCP,
        mp.solutions.hands.HandLandmark.PINKY_MCP
    ]
    
    for i in range(len(finger_tips)):
        if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_mcp[i]].y - 0.02:
            return False

    if len(finger_tips) > 0:
        for i in range(1, len(finger_tips)):
            if abs(hand_landmarks.landmark[finger_tips[0]].y - hand_landmarks.landmark[finger_tips[i]].y) > 0.05:
                return False
    else:
        return False
    
    if hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].y > hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_IP].y:
        return False
    
    highest_tip_y = min([hand_landmarks.landmark[tip].y for tip in finger_tips])
    
    if hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].y > highest_tip_y + 0.05: 
        return False

    distance = abs(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].x - hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP].x)

    if distance > 0.08:
        return False

    return True 