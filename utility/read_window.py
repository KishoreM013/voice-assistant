import pyautogui
import pytesseract
import pyttsx3
import time
import subprocess
import platform
from PIL import ImageGrab

def get_active_window_bbox():
    system = platform.system()
    
    if system == "Windows":
        import win32gui
        window = win32gui.GetForegroundWindow()
        rect = win32gui.GetWindowRect(window)  # (x, y, x2, y2)
        return rect
    
    elif system == "Linux":
        # Requires `xdotool` and `xwininfo` (install via pacman or apt)
        try:
            win_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()
            output = subprocess.check_output(["xwininfo", "-id", win_id]).decode()

            x = int([line for line in output.splitlines() if "Absolute upper-left X" in line][0].split(":")[1])
            y = int([line for line in output.splitlines() if "Absolute upper-left Y" in line][0].split(":")[1])
            width = int([line for line in output.splitlines() if "Width" in line][0].split(":")[1])
            height = int([line for line in output.splitlines() if "Height" in line][0].split(":")[1])
            return (x, y, x + width, y + height)
        except Exception as e:
            print("Error getting active window:", e)
            return None
    
    else:
        print("Unsupported OS")
        return None

def screenshot_and_read_text():
    time.sleep(1)  # short delay before capture
    bbox = get_active_window_bbox()

    if not bbox:
        print("Failed to get window bounds.")
        return

    screenshot = ImageGrab.grab(bbox=bbox)
    text = pytesseract.image_to_string(screenshot)

    if not text.strip():
        print("No text detected.")
        return

    print("Extracted text:")
    print(text)

    # Read it
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

screenshot_and_read_text()
