import mediapipe as mp
import numpy as np
mp_hands = mp.solutions.hands

def O(hand_landmarks):
    return True