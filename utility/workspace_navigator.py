import sys
import pyautogui
import time

def switch_workspace_by_shortcut(command):
    """
    Switches virtual desktops by simulating the built-in Windows keyboard shortcuts.
    Supports: 'next', 'prev', or a desktop number (1-based).
    """
    print("Executing workspace change by keyboard shortcut...")

    time.sleep(0.5)

    try:
        cmd_lower = command.lower()
        if cmd_lower == 'next':
            pyautogui.hotkey('ctrl', 'win', 'right')
            print("Switched to the next desktop.")
        elif cmd_lower == 'prev':
            pyautogui.hotkey('ctrl', 'win', 'left')
            print("Switched to the previous desktop.")
        elif command.isdigit() and int(command) > 0:
            target = int(command)
            print(f"Jumping to desktop {target}... (will go to left-most desktop first)")
            # Go to the left-most workspace (Desktop 1)
            for _ in range(20):  # Large enough to guarantee we hit Desktop 1
                pyautogui.hotkey('ctrl', 'win', 'left')
                time.sleep(0.01)
            # Now move to the desired desktop
            for _ in range(target - 1):
                pyautogui.hotkey('ctrl', 'win', 'right')
                time.sleep(0.01)
            print(f"Arrived at desktop {target}.")
        else:
            print(f"Error: Invalid command '{command}'. Use 'next', 'prev', or a positive number.")
    except Exception as e:
        print(f"An error occurred while simulating key presses: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python workspace.py [next|prev|number]")
        print("\nExamples:")
        print("  python workspace.py next")
        print("  python workspace.py prev")
        print("  python workspace.py 3")
    else:
        switch_workspace_by_shortcut(sys.argv[1])
