import subprocess
import re
import socket

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
NC = '\033[0m'

def get_ip_address():
    try:
        ip = subprocess.check_output(['ip', '-4', 'addr', 'show', 'scope', 'global'])
        ip = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', ip.decode()).group(1)
    except Exception:
        ip = subprocess.check_output(['ifconfig'])
        ip = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', ip.decode()).group(1)
    return ip

def get_network_range(ip):
    parts = ip.split('.')
    return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"

def run_command(command):
    try:
        return subprocess.check_output(command, shell=True).decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

def check_ports_and_vulnerabilities(ip):
    print(f"{YELLOW}Checking IP: {ip} for open FTP, SSH, and HTTP ports...{NC}")

    nmap_output = run_command(f"nmap -Pn -p 21,22,80 {ip}")
    
    if "21/tcp open" in nmap_output:
        print(f"{GREEN}---------------------------------{NC}")
        print(f"{GREEN}Found open FTP port on IP: {ip}{NC}")
        detailed_info = run_command(f"sudo nmap -sV -O {ip}")
        print(f"{BLUE}{detailed_info}{NC}")
        print(f"{GREEN}---------------------------------{NC}")
    else:
        print(f"{RED}FTP port closed on IP: {ip}{NC}")

    if "22/tcp open" in nmap_output:
        print(f"{GREEN}---------------------------------{NC}")
        print(f"{GREEN}Found open SSH port on IP: {ip}{NC}")
        detailed_info = run_command(f"sudo nmap -sV -O {ip}")
        print(f"{BLUE}{detailed_info}{NC}")
        print(f"{GREEN}---------------------------------{NC}")
    else:
        print(f"{RED}SSH port closed on IP: {ip}{NC}")

    if "80/tcp open" in nmap_output:
        print(f"{GREEN}---------------------------------{NC}")
        print(f"{GREEN}Found open HTTP port on IP: {ip}{NC}")
        detailed_info = run_command(f"sudo nmap -sV -O {ip}")
        print(f"{BLUE}{detailed_info}{NC}")
        print(f"{GREEN}---------------------------------{NC}")
    else:
        print(f"{RED}HTTP port closed on IP: {ip}{NC}")

    vulscan_output = run_command(f"sudo nmap --script vuln {ip}")
    print(f"{CYAN}{vulscan_output}{NC}")

def main():
    ip_address = get_ip_address()
    network = get_network_range(ip_address)

    print(f"{CYAN}Scanning network {network}...{NC}")
    ip_list = run_command(f"sudo netdiscover -r {network} -P | grep ' 1 ' | awk '{{print $1}}'").split()

    for ip in ip_list:
        check_ports_and_vulnerabilities(ip)

if __name__ == "__main__":
    main()
