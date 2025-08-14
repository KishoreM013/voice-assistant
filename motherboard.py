import speech_recognition as sr
import pyttsx3
import time
import os
from Worker import Worker  # Assuming Worker is defined in a separate module

# --- Configuration ---
WAKE_WORD = "friend"
LISTEN_TIMEOUT = 6
LOG_FILE = os.path.expanduser("~/motherboard.log")  # Logbook in home directory

class MotherBoard:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('rate', 150)
        self.is_awake = False
        self.worker = Worker()

        with self.microphone as source:
            self.log_event("Calibrating for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            self.log_event("Calibration complete.")

    def log_event(self, message):
        """Write a timestamped event to the log file."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(message)  # Still print for live view

    def speak(self, text):
        self.log_event(f"Assistant speaking: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen_for_audio(self, timeout=None):
        with self.microphone as source:
            try:
                self.log_event("Listening for audio...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                self.log_event("Recognizing speech...")
                command = self.recognizer.recognize_google(audio).lower()
                self.log_event(f"User said: {command}")
                return command
            except sr.WaitTimeoutError:
                self.log_event("Listening timed out.")
                return "timeout"
            except sr.UnknownValueError:
                self.log_event("Could not understand audio.")
                return None
            except sr.RequestError as e:
                self.log_event(f"API Request Error: {e}")
                self.speak("Could not request results from the service.")
                return None
            except Exception as e:
                self.log_event(f"Unexpected error: {e}")
                return None

    def start(self):
        self.speak("Assistant is now running in sleep mode.")
        
        while True:
            if self.is_awake:
                command = self.listen_for_audio(timeout=LISTEN_TIMEOUT)

                if command == "timeout":
                    self.speak("No command received. Going back to sleep.")
                    self.is_awake = False
                    continue
                elif command is not None:
                    if "hello" in command:
                        self.speak("Hello to you too!")
                    elif "what time is it" in command:
                        current_time = time.strftime("%I:%M %p")
                        self.speak(f"The current time is {current_time}")
                    elif "goodbye" in command or "go to sleep" in command:
                        self.speak("Goodbye! Going to sleep.")
                        self.is_awake = False
                    else:
                        self.log_event(f"Passing command to worker: {command}")
                        self.worker.act_on_command(command)
                    self.speak("Waiting for your next command.")
            else:
                wake_command = self.listen_for_audio()
                if wake_command and WAKE_WORD in wake_command:
                    self.is_awake = True
                    self.speak("Listening...")

if __name__ == "__main__":
    assistant = MotherBoard()
    assistant.start()
