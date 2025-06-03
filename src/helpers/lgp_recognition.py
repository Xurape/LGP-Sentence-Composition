import time
import helpers.gestures.saudations as saudations
import helpers.gestures.verbs as verbs
import helpers.gestures.letters as letters

class LGPRecognition:
    def __init__(self):
        self.gesture_dict = {
            # saudations
            "ola": saudations.hello,
            "adeus": saudations.goodbye,
            
            # verbs
            "sou": verbs.be,
            
            # letters
            "o": letters.O,
            "j": letters.J,
            "a": letters.A,
        }
    
    def add_gesture_to_sentence(self, gesture_name, sentence):
        if not sentence:
            # possivel adicionar mais gestos para meter ","
            if gesture_name in ["ola"]:
                sentence += f"{gesture_name.capitalize()}, "
            else:
                sentence += f"{gesture_name.capitalize()} "
        else:
            sentence += f"{gesture_name} "
            
        if "j o a o" in sentence or "J o a o" in sentence:
            sentence = sentence.replace("j o a o", "Joao")
            sentence = sentence.replace("J o a o", "Joao")
            
        return sentence

    def recognize(self, hand_landmarks):
        for name, pattern_fn in self.gesture_dict.items():
            if pattern_fn(hand_landmarks):
                return name
        return None