import sys
import pyautogui
import time
import os

def launch_application(app_name):
    """
    Launches an application by first trying a direct command,
    then falling back to GUI automation if the direct command might fail.
    """
    print(f"Attempting to open '{app_name}'...")

    # --- Method 1: Direct Command (Fast and Reliable) ---
    # This is the preferred method for known apps or apps in the system PATH.
    # The 'start' command is robust for this. We use os.system to run it.
    # The return code 0 usually indicates success.
    # We add empty quotes `""` as a best practice for the `start` command.
    # if os.system(f'start "" "{app_name}"') == 0:
    #     print(f"Successfully launched '{app_name}' using the start command.")
    #     return

    # --- Method 2: GUI Automation (Fallback) ---
    # If the start command fails (returns a non-zero exit code),
    # use pyautogui to simulate keyboard input as requested.
    print(f"Start command might have failed. Falling back to GUI automation...")
    try:
        # 1. Press the Windows key to open the Start Menu
        pyautogui.press('win')
        time.sleep(1)  # Wait for the Start Menu to appear

        # 2. Type the application name
        pyautogui.write(app_name, interval=0.05)
        time.sleep(1) # Wait for search results to appear

        # 3. Press Enter to launch the application
        pyautogui.press('enter')
        
        print(f"Sent keyboard commands to open '{app_name}'.")

    except Exception as e:
        print(f"An error occurred during GUI automation: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python launch_app.py \"<application_name>\"")
        print("\nExample:")
        print("  python launch_app.py \"notepad\"")
        print("  python launch_app.py \"Google Chrome\"")
    else:
        application_name = sys.argv[1]
        launch_application(application_name)
