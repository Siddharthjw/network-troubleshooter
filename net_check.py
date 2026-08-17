import socket, os, datetime, subprocess, re

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report = f"--- Network Report {time} ---\n"

gateway = "192.168.1.1"
try:
    output = subprocess.check_output("ipconfig", encoding="utf-8")
    match = re.search(r"Default Gateway.*?: (\d+\.\d+\.\d+\.\d+)", output)
    if match:
        gateway = match.group(1)
except:
    pass

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
report += f"Hostname: {hostname} | IP: {ip}\n"
report += f"Detected Gateway: {gateway}\n"

# 1. Gateway ping = Cable check
gw_ping = os.system(f"ping -n 1 {gateway} > nul")
report += f"Gateway {gateway} : {'OK - Cable/WiFi OK' if gw_ping==0 else 'FAIL - Check LAN Cable / WiFi'}\n"

# 2. Internet ping
dns_ping = os.system("ping -n 1 8.8.8.8 > nul")
report += f"Internet (8.8.8.8): {'OK' if dns_ping==0 else 'FAIL - No Internet / ISP Down'}\n"

# 3. Port check
s = socket.socket()
try:
    s.settimeout(3)
    s.connect(("google.com", 443))
    report += "Port 443 (HTTPS): OPEN - Service OK\n"
except:
    report += "Port 443: CLOSED - Firewall/Service issue\n"
s.close()

# Save
with open("network_report.txt", "a") as f:
    f.write(report + "\n")

print(report)
print("\nReport saved to network_report.txt")