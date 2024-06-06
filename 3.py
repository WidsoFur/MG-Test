import subprocess
import time
from datetime import datetime, timedelta

LOG_FILE = "/var/log/nginx/access.log"
BLOCK_THRESHOLD = 10 
TIME_WINDOW = 120  # 2 минуты
UNBLOCK_WINDOW = 600  # 10 минут

blocked_ips = {}

def parse_log():
    current_time = datetime.strptime("06/Jun/2024:12:03:55", "%d/%b/%Y:%H:%M:%S")
    recent_ips = {}

    with open(LOG_FILE, "r") as file:
        for line in file:
            parts = line.split()
            if len(parts) < 4:
                continue

            ip = parts[0]
            time_str = parts[3][1:]
            log_time = datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S")
            time_diff = (current_time - log_time).total_seconds()

            if time_diff <= TIME_WINDOW:
                if ip in recent_ips:
                    recent_ips[ip].append(log_time)
                else:
                    recent_ips[ip] = [log_time]

    return recent_ips

def block_ip(ip):
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        blocked_ips[ip] = datetime.now()
        print(f"Blocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block IP {ip}: {e}")

def unblock_ip(ip):
    try:
        subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        if ip in blocked_ips:
            del blocked_ips[ip]
        print(f"Unblocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to unblock IP {ip}: {e}")

def manage_blocked_ips(recent_ips):
    current_time = datetime.now()
    to_block = []
    to_unblock = []

    for ip, times in recent_ips.items():
        if len(times) > BLOCK_THRESHOLD and ip not in blocked_ips:
            to_block.append(ip)

    for ip in list(blocked_ips.keys()):
        if (current_time - blocked_ips[ip]).total_seconds() > UNBLOCK_WINDOW:
            to_unblock.append(ip)

    return to_block, to_unblock

if __name__ == "__main__":
    while True:
        recent_ips = parse_log()
        to_block, to_unblock = manage_blocked_ips(recent_ips)

        for ip in to_block:
            block_ip(ip)

        for ip in to_unblock:
            unblock_ip(ip)

        time.sleep(60) 
