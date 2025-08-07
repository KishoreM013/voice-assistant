# motherboard.py
from Recorder import AltSpeechRecognizer
from get_dependenies import DependencyCollector
from Worker import Worker
from reader import TextNarrator

class Motherboard:
    def __init__(self):
        self.collector = DependencyCollector()
        self.worker = Worker()
        self.narrator = TextNarrator()

        self.recognizer = AltSpeechRecognizer(callback=self._process_text)
        print("[Motherboard] Initialized. ALT = Speak | ESC = Exit")

    def _say(self, message: str):
        """Narrate and print a message."""
        print(f"[Motherboard] {message}")
        self.narrator.extract_and_speak(f"#{message}#")

    def _process_text(self, text: str):
        if not text.strip():
            self._say("I didn't catch that. Try again.")
            return

        self._say("Processing your command.")

        # Step 1: Get dependencies
        self._say("Checking system dependencies.")
        dep_result = self.collector.get_dependency(text)
        if dep_result and "No dependencies required." not in dep_result:
            self._say("Dependency check complete.")
            print(f"[Motherboard] Dependency Output:\n{dep_result}")
            self._narrate_if_needed(dep_result)
        else:
            self._say("No system dependencies needed.")

        # Step 2: Perform action
        self._say("Performing the requested action.")
        action_result = self.worker.act_on_command(text)
        if action_result and "No actionable" not in action_result:
            self._say("Action executed.")
            print(f"[Motherboard] Action Output:\n{action_result}")
            self._narrate_if_needed(action_result)
        else:
            self._say("No action was required.")

        self._say("Done. Ready for next command.")

    def _narrate_if_needed(self, message: str):
        narrated = self.narrator.extract_and_speak(message)
        if narrated:
            print(f"[Motherboard] Narrated: {narrated}")

    def run(self):
        self._say("System is live. Hold ALT and speak. Press escape to exit.")
        self.recognizer.run()

if __name__ == "__main__":
    Motherboard().run()
