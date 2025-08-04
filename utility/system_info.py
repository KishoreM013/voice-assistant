import platform
import socket
import psutil
import subprocess
import datetime
import pyautogui
import pygetwindow as gw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER

def get_system_info_text():
    """
    Gathers detailed system information for Windows and formats it into a single text block.
    Includes OS, Hardware, Network, Battery, Display, and Audio details.
    """
    
    # Helper to format bytes into a readable format (GB)
    def bytes_to_gb(b):
        return round(b / (1024**3), 2)

    # --- Start building the report string ---
    info_text = ""
    
    # 1. OS and Host Information
    uname = platform.uname()
    info_text += f"--- System Information ---\n"
    info_text += f"OS        : {uname.system} {uname.release} ({platform.win32_ver()[0]})\n"
    info_text += f"Arch      : {uname.machine}\n"
    info_text += f"Hostname  : {socket.gethostname()}\n"
    
    # 2. Uptime
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    days, rem = divmod(uptime.total_seconds(), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    info_text += f"Uptime    : {int(days)}d {int(hours)}h {int(minutes)}m\n"

    # 3. Motherboard (using WMIC)
    try:
        mobo_info = subprocess.check_output("wmic baseboard get product,Manufacturer", text=True, stderr=subprocess.DEVNULL).strip().split('\n')[-1].strip()
        info_text += f"Motherboard: {mobo_info}\n"
    except Exception:
        info_text += "Motherboard: Not Found\n"

    # 4. Hardware Section
    info_text += "\n--- Hardware ---\n"
    cpu_freq = psutil.cpu_freq()
    info_text += f"CPU       : {platform.processor()}\n"
    info_text += f"Cores     : {psutil.cpu_count(logical=False)} Physical, {psutil.cpu_count(logical=True)} Logical\n"
    info_text += f"CPU Usage : {psutil.cpu_percent()}% \n"
    try:
        gpu_info = subprocess.check_output("wmic path Win32_VideoController get Name", text=True, stderr=subprocess.DEVNULL).strip().split('\n')[-1].strip()
        info_text += f"GPU       : {gpu_info}\n"
    except Exception:
        info_text += "GPU       : Not Found\n"
    svmem = psutil.virtual_memory()
    info_text += f"Memory    : {bytes_to_gb(svmem.used)} GB / {bytes_to_gb(svmem.total)} GB ({svmem.percent}%)\n"
    
    # 5. Battery (only if present)
    battery = psutil.sensors_battery()
    if battery:
        info_text += "\n--- Battery ---\n"
        status = "Charging" if battery.power_plugged else "Discharging"
        time_left = "N/A"
        if not battery.power_plugged and battery.secsleft is not None:
            mins, secs = divmod(battery.secsleft, 60)
            hrs, mins = divmod(mins, 60)
            time_left = f"{hrs}h {mins}m left"
        info_text += f"Status    : {battery.percent}% ({status})\n"
        info_text += f"Time Left : {time_left}\n"
        
    # 6. Display and Audio
    info_text += "\n--- Display & Audio ---\n"
    try:
        screen_size = pyautogui.size()
        info_text += f"Resolution: {screen_size.width}x{screen_size.height}\n"
    except Exception:
        info_text += "Resolution: Not Found\n"
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_volume = int(volume.GetMasterVolumeLevelScalar() * 100)
        info_text += f"Audio     : {current_volume}% ({devices.FriendlyName})\n"
    except Exception:
        info_text += "Audio     : Not Found\n"

    # 7. Network Information
    info_text += "\n--- Network ---\n"
    addrs = psutil.net_if_addrs()
    for name, snics in addrs.items():
        for snic in snics:
            if snic.family == socket.AF_INET: # IPv4
                if "Loopback" not in name and "VMware" not in name and "VirtualBox" not in name:
                    info_text += f"Interface : {name}\n"
                    info_text += f"IP Address: {snic.address}\n"
                    break # Show first non-virtual IPv4 interface and move to next
    
    # 8. Storage
    info_text += "\n--- Storage ---\n"
    partitions = psutil.disk_partitions()
    for p in partitions:
        if p.fstype: # Only show mounted file systems
            try:
                usage = psutil.disk_usage(p.mountpoint)
                info_text += f"Disk ({p.mountpoint}) : {bytes_to_gb(usage.used)} GB / {bytes_to_gb(usage.total)} GB ({usage.percent}%)\n"
            except PermissionError:
                continue

    return info_text

if __name__ == "__main__":
    system_details = get_system_info_text()
    print(system_details)
    with open("system_report.txt", "w") as f:
        f.write(system_details)
    print("\nReport also saved to system_report.txt")
