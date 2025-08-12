import speech_recognition as sr
import pyttsx3
import time
from Worker import Worker  # Assuming Worker is defined in a separate module
# --- Configuration ---
WAKE_WORD = "friend"  # The word to wake up the assistant
LISTEN_TIMEOUT = 6    # Seconds to wait for a command before sleeping

class MotherBoard:
    """
    A voice assistant that waits for a wake word, listens for a command,
    and goes to sleep after a period of inactivity.
    """
    def __init__(self):
        """Initializes the recognizer and text-to-speech engine."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        self.tts_engine = pyttsx3.init()
        # Optional: Adjust voice properties
        voices = self.tts_engine.getProperty('voices')
        # self.tts_engine.setProperty('voice', voices[1].id) # Example: to select a female voice
        self.tts_engine.setProperty('rate', 150) # Speed of speech
        
        self.is_awake = False # The assistant starts in sleep mode
        self.worker = Worker()
        # Adjust recognizer for ambient noise
        with self.microphone as source:
            print("Calibrating for ambient noise, please wait...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            print("Calibration complete.")

    def speak(self, text):
        """Converts text to speech."""
        print(f"Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen_for_audio(self, timeout=None):
        """
        Listens for audio from the microphone and converts it to text.
        
        Args:
            timeout (int, optional): How long to wait for a phrase to start.
                                     If None, it waits indefinitely.
        
        Returns:
            str or None: The recognized text in lowercase, or None if not understood.
        """
        with self.microphone as source:
            try:
                print("Listening...")
                # The timeout parameter is key for the sleep functionality
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
                
                print("Recognizing...")
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
                
            except sr.WaitTimeoutError:
                # This error is triggered when listen() times out
                return "timeout"
            except sr.UnknownValueError:
                # This happens when speech is detected but not understood
                # We can ignore this and just keep listening
                return None
            except sr.RequestError as e:
                self.speak("Could not request results from the service.")
                print(f"API Error: {e}")
                return None
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return None

    def start(self):
        """The main loop for the voice assistant."""
        self.speak("Assistant is now running in sleep mode.")
        
        while True:
            if self.is_awake:
                # --- ACTIVE MODE ---
                # 1. Listen for a command with a timeout
                command = self.listen_for_audio(timeout=LISTEN_TIMEOUT)

                if command == "timeout":
                    # 2. If no command is heard, go to sleep
                    self.speak("No command received. Going back to sleep.")
                    self.is_awake = False
                    continue # Go to the next loop iteration (in sleep mode)
                
                elif command is not None:
                    # 3. If a command is heard, process it
                    # Here you can add your logic to handle different commands

                    if "hello" in command:
                        self.speak("Hello to you too!")
                    elif "what time is it" in command:
                        current_time = time.strftime("%I:%M %p")
                        self.speak(f"The current time is {current_time}")
                    elif "goodbye" in command or "go to sleep" in command:
                        self.speak("Goodbye! Going to sleep.")
                        self.is_awake = False
                    else:
                        self.worker.act_on_command(command)
                    
                    # After processing, stay awake and listen for the next command
                    self.speak("Waiting for your next command.")
                
            else:
                # --- SLEEP MODE ---
                # 1. Listen indefinitely for the wake word
                wake_command = self.listen_for_audio()

                # 2. If the wake word is detected, switch to active mode
                if wake_command and WAKE_WORD in wake_command:
                    self.is_awake = True
                    self.speak("Listening...")

# --- Main Execution ---
if __name__ == "__main__":
    assistant = MotherBoard()
    assistant.start()
