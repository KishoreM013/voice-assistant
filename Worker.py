import subprocess
import os
import re
from AI import ask_gemini
from reader import TextNarrator

class Worker:
    def __init__(self):
        self.narrator = TextNarrator()
        self.prompt_template = """You are a Windows 11 Action Automation Bot.

Your job is to generate Windows-compatible CMD batch scripts that perform direct **actions** on the device based on user intent.

You also have access to the following **Python utility scripts** (in the same directory), and you SHOULD use them whenever applicable:

✅ Available Utility Scripts:

1. **volume.py [level]** – Set or adjust system volume
   - Examples:
     - `python volume.py 50` → set volume to 50%
     - `python volume.py +10` → increase by 10%
     - `python volume.py -20` → decrease by 20%

2. **launch_app.py "App Name"** – Launch applications
   - Examples:
     - `python launch_app.py "notepad"`
     - `python launch_app.py "Google Chrome"`

3. **close_active.py** – Close the currently active application window

4. **workspace.py [next|prev|number]** – Switch virtual desktops/workspaces
   - Examples:
     - `python workspace.py next`
     - `python workspace.py 2`

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

    def act_on_command(self, user_text: str) -> str:
        if not user_text.strip():
            return "No action command detected."

        full_prompt = f"{self.prompt_template}\n\nUser command:\n{user_text.strip()}"
        ai_response = ask_gemini(full_prompt).strip()

        if ai_response.lower() == "--no":
            return "No actionable command required."

        narration = self._extract_narration(ai_response)
        if narration:
            self.narrator.extract_and_speak(f"#{narration}#")

        script = self._extract_script(ai_response)

        if not script:
            return "Failed to extract script from AI response."

        # Clean up before executing
        self._clean_file("run.bat")

        with open("run.bat", "w", encoding="utf-8") as f:
            f.write(script)

        try:
            subprocess.run(["cmd.exe", "/c", "run.bat"], check=True)
        except subprocess.CalledProcessError as e:
            return f"Error executing script: {e}"

        self._clean_file("run.bat")

        return f"✅ Action completed: {narration}"

    def _extract_narration(self, text: str) -> str:
        match = re.search(r"#(.*?)#", text, re.DOTALL)
        return match.group(1).strip() if match else ""

    def _extract_script(self, text: str) -> str:
        # Remove all text up to and including the last '#'
        parts = text.rsplit("#", maxsplit=2)
        return parts[-1].strip() if len(parts) >= 2 else ""

    def _clean_file(self, filename: str):
        if os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                f.write("")
