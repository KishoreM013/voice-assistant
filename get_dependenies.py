import subprocess
import re
import os
from AI import ask_gemini
from reader import TextNarrator


class DependencyCollector:
    def __init__(self):
        self.narrator = TextNarrator()
        print("DependencyCollector initialized. Ready to collect dependencies.")

        self.prompt_template = """You are a Windows 11 CMD Script Generator Bot.

Your job is to determine whether the user's request requires collecting system-level information ("dependencies") from their device.

✅ If dependencies ARE required (e.g., battery level, Wi-Fi status, file/folder search, disk usage, etc.):

    First, output a short human-readable text describing the process that will run in the background. Format this text as:
    # your short message here #

    Then, output only a valid Windows CMD batch script that collects the needed information and saves it to a file named dep.txt.

    ⚠️ Do NOT use deprecated tools like WMIC.
    ✅ You may use PowerShell commands if called *through CMD* (e.g., `powershell -Command "..."`)
    ✅ Only use commands/tools that are available by default in a typical Windows 11 installation.
    ❌ Do NOT use Bash, Linux commands, or any third-party/external utilities.

❌ If dependencies are NOT required (e.g., opening/closing apps, changing brightness, adjusting volume, launching websites):

    Return exactly this: --no

☑️ Do NOT include any markdown formatting, code blocks, or explanations.
☑️ Only output:

    # short message # followed by raw CMD script

    OR --no

🧠 After running the script, the user will provide the contents of dep.txt along with their original request. You will use this to generate the final response.

The system is Windows 11, and all commands will be run inside Command Prompt (CMD) — not PowerShell or Bash."""

    def clean_files(self):
        for filename in ["run.bat", "dep.txt"]:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("")

    def get_dependency(self, user_text: str) -> str:
        if not user_text.strip():
            return "No command detected."

        self.clean_files()
        print(f"User request: {user_text.strip()}")

        full_prompt = f"{self.prompt_template}\n\nthe user given text goes here:\n{user_text.strip()}"
        ai_response = ask_gemini(full_prompt).strip()

        if ai_response.lower() == "--no":
            return "No dependencies required."

        # Extract the first #...# message
        match = re.search(r"#(.*?)#", ai_response, re.DOTALL)
        message = match.group(1).strip() if match else "Running dependency collection..."
        self.narrator.extract_and_speak(ai_response)


        # Get the script after the second #
        script_start = ai_response.find("#", ai_response.find("#") + 1)
        script = ai_response[script_start + 1:].strip()

        with open("run.bat", "w", encoding="utf-8") as f:
            f.write(script)

        try:
            subprocess.run(["cmd.exe", "/c", "run.bat"], check=True)
        except subprocess.CalledProcessError as e:
            return f"Script execution failed: {e}"

        result = ""
        if os.path.exists("dep.txt"):
            with open("dep.txt", "r", encoding="utf-8", errors="ignore") as f:
                result = f.read().strip()

        self.clean_files()
        return result or "Dependency script ran but produced no output."


if __name__ == "__main__":
    collector = DependencyCollector()
    user_input = "Check battery status"
    output = collector.get_dependency(user_input)
    print("Output:", output)
    