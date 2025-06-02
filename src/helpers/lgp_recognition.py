import numpy as np
import helpers.gestures.saudations as saudations
import helpers.gestures.verbs as verbs
import helpers.gestures.letters as letters

class LGPRecognition:
    def __init__(self):
        self.gesture_dict = {
            # saudations
            "Ola": saudations.hello,
            "Adeus": saudations.goodbye,
            
            # verbs
            "Sou": verbs.be,
            
            # letters
            "O": letters.O
        }

    def recognize(self, hand_landmarks):
        for name, pattern_fn in self.gesture_dict.items():
            if pattern_fn(hand_landmarks):
                return name
        return None