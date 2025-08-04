import sys
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def set_volume(level_str):
    """
    Sets or adjusts the system master volume.
    Accepts an absolute number (e.g., "50") or a relative adjustment (e.g., "+10", "-10").
    """
    try:
        # Get the default audio playback device
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        # Check if the argument is for relative adjustment
        if level_str.startswith('+') or level_str.startswith('-'):
            current_volume_scalar = volume.GetMasterVolumeLevelScalar()
            adjustment = float(level_str) / 100.0
            new_volume_scalar = current_volume_scalar + adjustment
            print(f"Adjusting volume by {level_str}%...")
        
        # Otherwise, assume it's an absolute level
        else:
            target_level = float(level_str)
            new_volume_scalar = target_level / 100.0
            print(f"Setting volume to {int(target_level)}%...")

        # Clamp the volume level to the valid range [0.0, 1.0]
        new_volume_scalar = max(0.0, min(1.0, new_volume_scalar))
        
        # Set the new volume
        volume.SetMasterVolumeLevelScalar(new_volume_scalar, None)
        
        print(f"Volume is now at {int(new_volume_scalar * 100)}%")

    except ValueError:
        print("Error: Please provide a valid number (e.g., '50', '+10', '-10').")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python volume.py [level]")
        print("  level: A number from 0 to 100, or a relative adjustment like '+10' or '-10'.")
        print("\nExamples:")
        print("  python volume.py 75    # Sets volume to 75%")
        print("  python volume.py +10   # Increases volume by 10%")
        print("  python volume.py -20   # Decreases volume by 20%")
    else:
        set_volume(sys.argv[1])
