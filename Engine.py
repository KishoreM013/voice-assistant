import speech_recognition as sr
import keyboard
import threading

class Engine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_data = None
        self.is_recording = False
        self.mic = sr.Microphone()
        print("Engine initialized. Hold ALT to record, release ALT to recognize and process.")

    def _record_audio(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
            print("Recording... (Hold ALT)")
            self.audio_data = self.recognizer.listen(source)
            print("Stopped Recording.")

    def _on_alt_press(self, event):
        if not self.is_recording:
            self.is_recording = True
            self.audio_data = None
            threading.Thread(target=self._record_audio, daemon=True).start()

    def _on_alt_release(self, event):
        if self.is_recording:
            self.is_recording = False
            # Recognize and act, in its own thread to avoid UI freeze
            threading.Thread(target=self.recognize_and_act, daemon=True).start()

    def recognize_and_act(self):
        if self.audio_data is not None:
            try:
                print("Recognizing...")
                text = self.recognizer.recognize_google(self.audio_data)
                print("Recognized Text:", text)
                self.handle_command(text)
            except sr.UnknownValueError:
                print("Sorry, could not understand audio.")
                self.handle_command("")
            except sr.RequestError as err:
                print(f"Recognition Error: {err}")
                self.handle_command("")
        else:
            print("No audio to transcribe.")

    def handle_command(self, text):
        """
        This is where you handle what happens after recognition.
        Customize as needed!
        """
        print(f"[ENGINE HOOK] You can now process this text: '{text}'")
        # TODO: Add your assistant logic here.
        # Example: if "weather" in text: call_weather_module()

    def run(self):
        keyboard.on_press_key('alt', self._on_alt_press)
        keyboard.on_release_key('alt', self._on_alt_release)
        print("Ready! Hold ALT and speak, release ALT to transcribe. ESC to exit.")
        try:
            keyboard.wait('esc')
        except KeyboardInterrupt:
            print("\nExiting Engine.")

if __name__ == "__main__":
    Engine().run()
