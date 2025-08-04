import platform
import socket
import psutil
import subprocess
import datetime
import pyautogui
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER

# GPU detection is now handled by GPUtil
try:
    import GPUtil
    gputil_available = True
except ImportError:
    gputil_available = False

def get_wifi_ssid():
    """Retrieves the connected Wi-Fi SSID using 'netsh'."""
    try:
        output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], text=True, stderr=subprocess.DEVNULL)
        for line in output.split('\n'):
            if 'SSID' in line and 'BSSID' not in line:
                return line.split(':')[1].strip()
    except Exception:
        return None
    return None

def bytes_to_human_readable(b):
    """Converts bytes into a human-readable format (GB, MB, KB)."""
    if b is None: return "N/A"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if b < 1024.0:
            return f"{b:.2f} {unit}"
        b /= 1024.0
    return f"{b:.2f} PB"

def get_detailed_system_info():
    """Gathers an extensive list of system details and formats them."""
    
    info_parts = []

    # --- System & OS ---
    uname = platform.uname()
    info_parts.append("--- System & OS ---")
    info_parts.append(f"OS              : {uname.system} {uname.release} ({platform.win32_ver()[0]})")
    info_parts.append(f"Architecture    : {uname.machine}")
    info_parts.append(f"Hostname        : {socket.gethostname()}")
    bt = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - bt
    info_parts.append(f"Boot Time       : {bt.strftime('%Y-%m-%d %H:%M:%S')}")
    info_parts.append(f"System Uptime   : {str(uptime).split('.')[0]}")

    # --- CPU ---
    info_parts.append("\n--- CPU ---")
    info_parts.append(f"Model           : {platform.processor()}")
    info_parts.append(f"Physical Cores  : {psutil.cpu_count(logical=False)}")
    info_parts.append(f"Logical Cores   : {psutil.cpu_count(logical=True)}")
    freq = psutil.cpu_freq()
    info_parts.append(f"Max Frequency   : {freq.max:.2f} Mhz")
    info_parts.append(f"Current Freq.   : {freq.current:.2f} Mhz")
    info_parts.append(f"Total CPU Usage : {psutil.cpu_percent(interval=1)}%")
    
    # --- GPU (Corrected) ---
    info_parts.append("\n--- GPU ---")
    if gputil_available:
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                for i, gpu in enumerate(gpus):
                    info_parts.append(f"GPU {i+1}           : {gpu.name}")
                    info_parts.append(f"  - Load        : {gpu.load*100:.1f}%")
                    info_parts.append(f"  - Temp        : {gpu.temperature} °C")
                    info_parts.append(f"  - Memory Used : {bytes_to_human_readable(gpu.memoryUsed*1024*1024)} / {bytes_to_human_readable(gpu.memoryTotal*1024*1024)}")
            else:
                 info_parts.append("GPU             : No NVIDIA GPU detected by GPUtil.")
        except Exception as e:
            info_parts.append(f"GPU             : Error getting GPU details - {e}")
    else:
        info_parts.append("GPU             : GPUtil library not installed. Cannot get NVIDIA details.")


    # --- Memory (RAM) ---
    mem = psutil.virtual_memory()
    info_parts.append("\n--- Memory (RAM) ---")
    info_parts.append(f"Total           : {bytes_to_human_readable(mem.total)}")
    info_parts.append(f"Available       : {bytes_to_human_readable(mem.available)}")
    info_parts.append(f"Used            : {bytes_to_human_readable(mem.used)} ({mem.percent}%)")

    # --- Network ---
    info_parts.append("\n--- Network ---")
    wifi_name = get_wifi_ssid()
    if wifi_name:
        info_parts.append(f"Wi-Fi SSID      : {wifi_name}")
    
    for if_name, if_addrs in psutil.net_if_addrs().items():
        if "Loopback" in if_name: continue
        for addr in if_addrs:
            if addr.family == socket.AF_INET:
                info_parts.append(f"Interface       : {if_name} (IP: {addr.address})")

    # --- Storage ---
    info_parts.append("\n--- Storage ---")
    for part in psutil.disk_partitions():
        if part.fstype and 'fixed' in part.opts:
            try:
                usage = psutil.disk_usage(part.mountpoint)
                info_parts.append(f"Disk ({part.mountpoint})      : {bytes_to_human_readable(usage.used)} / {bytes_to_human_readable(usage.total)} ({usage.percent}%)")
            except PermissionError:
                continue

    return "\n".join(info_parts)

if __name__ == "__main__":
    system_report = get_detailed_system_info()
    print(system_report)
    with open("deep_system_report.txt", "w") as f:
        f.write(system_report)
    print("\nFull report also saved to deep_system_report.txt")
