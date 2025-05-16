import numpy as np
import helpers.gestures.verbs as verbs

class LGPRecognition:
    def __init__(self):
        self.gesture_dict = {
            "Ola": verbs.hello,
        }

    def recognize(self, hand_landmarks):
        for name, pattern_fn in self.gesture_dict.items():
            if pattern_fn(hand_landmarks):
                return name
        return None