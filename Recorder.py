import threading
import time
import speech_recognition as sr

class HotwordListener:
    def __init__(self, hotword="slave", command_timeout=6, callback=None):
        self.hotword = hotword.lower()
        self.command_timeout = command_timeout
        self.callback = callback

        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

        self.listening = True  # overall loop control
        self.active = False    # True when command listening active after hotword
        self.paused = False    # pause listening during TTS

        self.thread = threading.Thread(target=self._background_listen, daemon=True)
        self.thread.start()

    def _background_listen(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        while self.listening:
            if self.paused:
                time.sleep(0.1)
                continue

            if not self.active:
                with self.mic as source:
                    print("[HotwordListener] Listening for hotword...")
                    audio = self.recognizer.listen(source, phrase_time_limit=3)
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"[HotwordListener] Heard: {text}")
                    if self.hotword in text:
                        print(f"[HotwordListener] Hotword '{self.hotword}' detected.")
                        self.active = True

                        # Pause listening during TTS
                        self.paused = True
                        if self.callback:
                            self.callback(f"Hotword '{self.hotword}' detected. What can I do for you?")
                        
                        # Wait 2 seconds after TTS before listening for command
                        time.sleep(2)
                        self.paused = False

                        self._listen_for_command()
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"[HotwordListener] API error: {e}")
            else:
                time.sleep(0.1)

    def _listen_for_command(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("[HotwordListener] Listening for command...")
            try:
                audio = self.recognizer.listen(source, timeout=self.command_timeout, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("[HotwordListener] No speech detected during command timeout.")
                if self.callback:
                    self.callback("")  # empty command, timeout
                self.active = False
                return
        try:
            command_text = self.recognizer.recognize_google(audio)
            print(f"[HotwordListener] Command recognized: {command_text}")
            if self.callback:
                self.callback(command_text)
        except sr.UnknownValueError:
            print("[HotwordListener] Could not understand command.")
            if self.callback:
                self.callback("")
        except sr.RequestError as e:
            print(f"[HotwordListener] API error during command recognition: {e}")
            if self.callback:
                self.callback("")
        self.active = False

    def stop(self):
        self.listening = False
        self.thread.join()
