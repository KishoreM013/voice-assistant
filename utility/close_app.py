import sys
import os

def close_safely(process_name):
    """
    Safely closes an application by its exact process name using the taskkill command.
    This is the most reliable and direct method.
    """
    # For consistency, we can ensure the name ends with .exe, though taskkill is often smart enough.
    if not process_name.lower().endswith('.exe'):
        process_name += '.exe'
        
    print(f"Attempting to close all processes with the exact name: '{process_name}'")
    
    # Construct the definitive command for closing an application by its image name.
    # /IM: Specifies the Image Name. This looks for an exact match.
    # /F: Forcefully terminates the process(es).
    # /T: Terminates the process and any child processes it started.
    command = f'taskkill /F /IM "{process_name}" /T'
    
    # Execute the command. The output from taskkill itself will tell you if it succeeded
    # or if the process was not found.
    os.system(command)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python close.py \"<process_name.exe>\"")
        print("\nDescription: Safely closes an application by its exact process name.")
        print("\nExamples:")
        print("  python close.py chrome.exe")
        print("  python close.py Taskmgr.exe")
    else:
        app_to_close = sys.argv[1]
        close_safely(app_to_close)
