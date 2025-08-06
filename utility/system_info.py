import platform
import psutil
import socket
import getpass
import os

def get_system_info():
    info = {}

    # OS and Architecture
    info['OS'] = f"{platform.system()} {platform.release()} ({platform.version()})"
    info['Architecture'] = platform.machine()

    # CPU Info
    info['Processor'] = platform.processor()
    info['Cores (Physical)'] = psutil.cpu_count(logical=False)
    info['Cores (Logical)'] = psutil.cpu_count(logical=True)

    # RAM
    ram = psutil.virtual_memory()
    info['RAM (Total)'] = f"{ram.total / 1e9:.2f} GB"
    info['RAM (Available)'] = f"{ram.available / 1e9:.2f} GB"

    # Disk
    disk = psutil.disk_usage('/')
    info['Disk (Total)'] = f"{disk.total / 1e9:.2f} GB"
    info['Disk (Used)'] = f"{disk.used / 1e9:.2f} GB"
    info['Disk (Free)'] = f"{disk.free / 1e9:.2f} GB"

    # Network (basic)
    hostname = socket.gethostname()
    info['Hostname'] = hostname
    info['IP Address'] = socket.gethostbyname(hostname)

    try:
        mac = ':'.join(['{:02X}'.format((psutil.net_if_addrs()['Wi-Fi'][0].address.encode()[i]) if isinstance(psutil.net_if_addrs()['Wi-Fi'][0].address, str) else 0) for i in range(6)])
        info['MAC Address'] = mac
    except:
        info['MAC Address'] = "Not found"

    # User
    info['User'] = getpass.getuser()

    # Battery
    battery = psutil.sensors_battery()
    if battery:
        info['Battery'] = f"{battery.percent}% {'(Plugged In)' if battery.power_plugged else '(On Battery)'}"
    else:
        info['Battery'] = "No battery info available"

    return info


if __name__ == "__main__":
    system_info = get_system_info()
    print("--- System Information ---")
    for k, v in system_info.items():
        print(f"{k}: {v}")
