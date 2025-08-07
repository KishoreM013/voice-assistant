import pyttsx3
import re
import threading

class TextNarrator:
    def __init__(self, rate: int = 190, voice_index: int = 0):
        self.engine = pyttsx3.init()
        print("TextNarrator initialized. Ready to speak.")
        self.engine.setProperty('rate', rate)
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[voice_index].id)

    def extract_and_speak(self, ai_text: str):
        """
        Extracts text between #...# and reads it out loud in a separate thread.
        """
        message = self._extract_message(ai_text)
        print(f"Extracted message: {message}")
        if message:
            threading.Thread(target=self._speak, args=(message,), daemon=True).start()
            return message
        return "No readable message found."

    def _extract_message(self, text: str) -> str:
        match = re.search(r"#(.*?)#", text, re.DOTALL)
        return match.group(1).strip() if match else ""

    def _speak(self, message: str):
        print(f"Speaking message: {message}")
        self.engine.say(message)
        self.engine.runAndWait()
