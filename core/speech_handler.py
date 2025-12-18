# aitalk_sql_assistant/core/speech_handler.py

import speech_recognition as sr
import pyttsx3

class SpeechHandler:
    def __init__(self):
        try:
            self.tts_engine = pyttsx3.init()
        except Exception:
            self.tts_engine = None
            print("Warning: pyttsx3 initialization failed. Text-to-speech will be disabled.")
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        if self.tts_engine:
            self.tts_engine.say(str(text))
            self.tts_engine.runAndWait()

    def listen_for_query(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source)
            text = self.recognizer.recognize_google(audio)
            return text, None
        except sr.UnknownValueError:
            return None, "Could not understand audio"
        except sr.RequestError as e:
            return None, f"Speech service unavailable: {e}"
        except Exception as e:
            return None, f"Microphone error: {e}"
