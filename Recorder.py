# Recorder.py
import speech_recognition as sr
import keyboard
import threading

class AltSpeechRecognizer:
    def __init__(self, callback=None):
        self.recognizer = sr.Recognizer()
        self.recording = False
        self.audio_data = None
        self.mic = sr.Microphone()
        self.callback = callback  # function to call with the recognized text
        print("AltSpeechRecognizer initialized. Hold Alt to record speech.")

    def _record(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
            print("Recording... (Keep Alt pressed)")
            self.audio_data = self.recognizer.listen(source)
            print("Recording stopped.")

    def _on_alt_press(self, e):
        if not self.recording:
            self.recording = True
            self.audio_data = None
            threading.Thread(target=self._record, daemon=True).start()

    def _on_alt_release(self, e):
        if self.recording:
            self.recording = False
            if self.audio_data is not None:
                threading.Thread(target=self._recognize_and_callback, daemon=True).start()
            else:
                print("No audio captured.")

    def _recognize_and_callback(self):
        try:
            print("Recognizing speech...")
            text = self.recognizer.recognize_google(self.audio_data)
            print("You said:", text)
            if self.callback:
                self.callback(text)
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
            if self.callback:
                self.callback("")
        except sr.RequestError as err:
            print(f"Could not request results; {err}")
            if self.callback:
                self.callback("")

    def run(self):
        keyboard.on_press_key('alt', self._on_alt_press)
        keyboard.on_release_key('alt', self._on_alt_release)
        print("Ready. Hold Alt and speak, release to transcribe. Press ESC to exit.")
        try:
            keyboard.wait('esc')
        except KeyboardInterrupt:
            print("Exiting...")
