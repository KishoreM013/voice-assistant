import subprocess
import os
import re
import time
from AI import ask_gemini
from get_dependenies import DependencyCollector
from reader import TextNarrator

LOG_FILE = os.path.expanduser("~/motherboard.log")  # Shared log file

class Worker:
    def __init__(self):
        self.narrator = TextNarrator()
        self.dependency_collector = DependencyCollector()
        self.prompt_template = """You are a Windows 11 Action Automation Bot.

Your job is to generate Windows-compatible CMD batch scripts that perform direct **actions** on the device based on user intent.

You also have access to the following **Python utility scripts** (in the same directory), and you SHOULD use them whenever applicable:

✅ Available Utility Scripts:

1. **C:/Utils/volume.py [level]** – Set or adjust system volume
   - Examples:
     - `python C:/Utils/volume.py 50` → set volume to 50%
     - `python C:/Utils/volume.py +10` → increase by 10%
     - `python C:/Utils/volume.py -20` → decrease by 20%

2. **C:/Utils/launch_app.py "App Name"** – Launch applications
   - Examples:
     - `python C:/Utils/launch_app.py "notepad"`
     - `python C:/Utils/launch_app.py "Google Chrome"`

3. **C:/Utils/close_active.py** – Close the currently active application window

4. **C:/Utils/workspace_navigator.py [next|prev|number]** – Switch virtual desktops/workspaces
   - Examples:
     - `python C:/Utils/workspace_navigator.py next`
     - `python C:/Utils/workspace_navigator.py 2`

👉 You must prefer using these scripts instead of writing native CMD commands when the task matches.

🧠 Otherwise, generate raw CMD-compatible batch script that performs the required action.

🗣️ Format your output as:

    # short description of what will happen #

    [CMD/Bash script here using either utilities or native commands]

❌ If no action is required (like a data query or information gathering), return exactly this: --no

⛔ Do NOT include:
- Any markdown formatting
- Any explanation
- Any labels like "script:", etc.

Only return:

    # narration #
    command...

    OR: --no

All commands will be executed using Windows CMD (or Git Bash if required).
"""

        self.log_event("Worker initialized and ready.")

    def log_event(self, message):
        """Log events with timestamps and class tag."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [Worker] {message}\n")
        print(f"[Worker] {message}")

    def act_on_command(self, user_text: str) -> str:
        if not user_text.strip():
            self.log_event("No action command detected.")
            return "No action command detected."

        self.log_event(f"Received command: {user_text.strip()}")
        dependency = self.dependency_collector.get_dependency(user_text) or ""
        self.log_event(f"Dependency data collected ({len(dependency)} characters).")

        full_prompt = f"{self.prompt_template}\n\nDependency:\n{dependency}\n\nUser command:\n{user_text.strip()}"
        ai_response = ask_gemini(full_prompt).strip()
        self.log_event(f"AI response received ({len(ai_response)} characters).")

        if ai_response.lower() == "--no":
            self.log_event("No actionable command required.")
            return "No actionable command required."

        narration = self._extract_narration(ai_response)
        if narration:
            self.log_event(f"Narration extracted: {narration}")
            self.narrator.extract_and_speak(narration)

        script = self._extract_script(ai_response)
        if not script:
            self.log_event("Failed to extract script from AI response.")
            return "Failed to extract script from AI response."

        with open("run.bat", "w", encoding="utf-8") as f:
            f.write(script)
        self.log_event("run.bat written with action script.")

        try:
            subprocess.run(["cmd.exe", "/c", "run.bat"], check=True)
            self.log_event("Script executed successfully.")
        except subprocess.CalledProcessError as e:
            self.log_event(f"Error executing script: {e}")
            return f"Error executing script: {e}"

        return f"✅ Action completed: {narration}"

    def _extract_narration(self, text: str) -> str:
        match = re.search(r"#(.*?)#", text, re.DOTALL)
        return match.group(1).strip() if match else ""

    def _extract_script(self, text: str) -> str:
        parts = text.rsplit("#", maxsplit=2)
        return parts[-1].strip() if len(parts) >= 2 else ""

    def _clean_file(self, filename: str):
        if os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                f.write("")
            self.log_event(f"File {filename} cleaned.")
