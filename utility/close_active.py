import pygetwindow as gw
import time

def close_active_window_safely():
    """
    Identifies the currently active window and sends a close command to it.
    This method is independent of the Fn key status on laptops.
    """
    try:
        # Give the user time to select the target window
        print("You have 5 seconds to click on the window you want to close...")
        for i in range(2, 0, -1):
            print(f"{i}...", end="", flush=True)
            time.sleep(1)
        print("\nSending close command.")

        # Get the currently active window
        active_window = gw.getActiveWindow()

        if active_window:
            print(f"Found active window: '{active_window.title}'")
            # This sends a graceful close request, just like clicking the 'X' button or pressing Alt+F4
            active_window.close()
            print("Close command sent successfully.")
        else:
            print("Could not identify an active window. No action taken.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have run 'pip install pygetwindow'.")

if __name__ == "__main__":
    close_active_window_safely()
