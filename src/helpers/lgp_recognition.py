import os
import json
import time
import helpers.gestures.saudations as saudations
import helpers.gestures.verbs as verbs
import helpers.gestures.letters as letters
import helpers.gestures.numbers as numbers
from helpers.lgp_gesture_creator import LGPGestureCreator

class LGPRecognition:
    def __init__(self):
        self.gesture_dict = {
            # saudations
            "ola": saudations.hello,
            "adeus": saudations.goodbye,
            
            # verbs
            "sou": verbs.be,
            "want": verbs.want,
            
            # letters
            "o": letters.O,
            "j": letters.J,
            "a": letters.A,
            
            # numbers
            "um": numbers.one,
        }
        
        self.custom_gesture_creator = LGPGestureCreator()
        self.custom_gestures = self._load_all_custom_gestures()

    def _load_all_custom_gestures(self):
        gestures = {}
        custom_dir = os.path.join(os.path.dirname(__file__), "gestures", "custom")
        
        if not os.path.exists(custom_dir):
            os.makedirs(custom_dir)
            
        for filename in os.listdir(custom_dir):
            if filename.endswith(".json"):
                with open(os.path.join(custom_dir, filename)) as f:
                    gesture_data = json.load(f)
                    gestures[gesture_data["name"]] = gesture_data
                    
        return gestures
    
    def update_gestures(self):
        self.custom_gestures = self._load_all_custom_gestures()
        print(f"[DEBUG] Gestos personalizados atualizados: {len(self.custom_gestures)} gestos carregados.")
    
    def add_gesture_to_sentence(self, gesture_name, sentence):
        if not sentence:
            #? possivel adicionar mais gestos para meter ","
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
            
        for name, gesture_data in self.custom_gestures.items():
            if self.custom_gesture_creator.match_gesture(hand_landmarks, gesture_data):
                return name
        return None