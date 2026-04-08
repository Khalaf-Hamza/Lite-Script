import datetime
import subprocess
from config import RED, GREEN, YELLOW, RESET
from utils import (
    safe_import, is_linux, run_command, sanitize_input, wait_for_input, 
    handle_menu_choice, is_valid_ip, is_valid_subnet, is_valid_port,
    is_interface_up, simple_loading_animation, netifaces
)
from loading import start_loading, stop_loading
from ui import logo, print_menu_header, print_menu_option

try:
    import requests
except ImportError:
    safe_import("requests")
    import requests

def networking():
    """Network tools menu."""
    # Local import to avoid circular dependency
    from main import auxop

    print_menu_header("Network Tools")
    print_menu_option("1", "View Network Interfaces")
    print_menu_option("2", "Display MAC Address")
    print_menu_option("3", "Change MAC Address")
    print_menu_option("4", "Host Discovery")
    print_menu_option("5", "DNS Lookup")
    print_menu_option("6", "Show Public IP Address")
    print_menu_option("7", "Port Scanning")
    print_menu_option("8", "Live Packet Capture")
    print_menu_option("9", "Vulnerability Scanning (Requires root)")

    option = input(f"{GREEN}Select an option or Enter to go back, '%' to exit: {RESET}")

    menu_actions = {
        "1": view_network_interfaces,
        "2": display_mac_address,
        "3": change_mac_address,
        "4": host_discovery,
        "5": dns_lookup,
        "6": show_public_ip,
        "7": port_scanning,
        "8": live_packet_capture,
        "9": vuln_scan,
    }

    if option in menu_actions:
        menu_actions[option]()
    elif not handle_menu_choice(option, auxop):
        print("Invalid option.")
        networking()


def view_network_interfaces():
    """Display all network interfaces."""
    logo()
    print("Displays all network interfaces on your system.")
    print("\nNetwork Interfaces:\n")
    
    if is_linux():
        run_command(["ip", "a"])
    else:
        run_command(["ipconfig"])
    
    wait_for_input(networking)


def display_mac_address():
    """Display MAC address of an interface."""
    logo()
    print("Displays MAC addresses of your network interfaces.")
    
    interface = sanitize_input(input("\nEnter interface name (e.g., eth0): "))
    if not interface:
        print("No interface specified.")
        wait_for_input(networking)
        return
    
    start_loading("Reading MAC address", style="cyber")
    result = run_command(["macchanger", "-s", interface], capture_output=True)
    stop_loading()
    
    if result and result.stdout:
        print(f"{RED}Current MAC: {interface} ({result.stdout.strip()}){RESET}")
    else:
        print(f"{RED}Could not get MAC address. Is macchanger installed?{RESET}")
    
    wait_for_input(networking)


def change_mac_address():
    """Change MAC address of an interface."""
    logo()
    print("Change the MAC address of a network interface (MAC spoofing).")
    
    interface = sanitize_input(input("\nEnter interface name (e.g., eth0): "))
    if not interface:
        print("No interface specified.")
        wait_for_input(networking)
        return
    
    new_mac = input("Enter new MAC (e.g., 00:11:22:33:44:55) or 'r' for random: ").strip()
    
    # Bring interface down
    run_command(["sudo", "ifconfig", interface, "down"])
    
    # Fixed: proper comparison for random MAC
    if new_mac.lower() == 'r':
        run_command(["sudo", "macchanger", "-r", interface])
    else:
        new_mac = sanitize_input(new_mac)
        if new_mac:
            run_command(["sudo", "macchanger", "-m", new_mac, interface])
    
    # Bring interface up
    run_command(["sudo", "ifconfig", interface, "up"])
    print(f"MAC address change attempted for {interface}.")
    
    wait_for_input(networking)


def host_discovery():
    """Discover hosts on a network subnet."""
    logo()
    print("Identifies active hosts on a network.")
    
    subnet = sanitize_input(input("\nEnter subnet (e.g., 192.168.0.0/24): "))
    
    # Fixed: actually use the validation result
    if not is_valid_subnet(subnet):
        print(f"{RED}Invalid subnet format.{RESET}")
        wait_for_input(networking)
        return
    
    print(f"\nDiscovering hosts in {subnet}...\n")
    run_command(["nmap", "-sn", subnet])  # -sn is preferred over deprecated -sP
    
    wait_for_input(networking)


def dns_lookup():
    """Perform DNS lookup."""
    logo()
    print("Resolves domain names to IP addresses and vice versa.")
    
    query = sanitize_input(input("\nEnter domain name or IP address: "))
    if not query:
        print("No query specified.")
        wait_for_input(networking)
        return
    
    print(f"\nPerforming DNS lookup for {query}...\n")
    run_command(["nslookup", query])
    
    wait_for_input(networking)


def show_public_ip():
    """Display public IP address."""
    logo()
    print("Displays your public IP address as seen from the internet.")
    print("\nPublic IP Address:\n")
    
    start_loading("Fetching public IP", style="dots")
    
    # Use requests instead of curl for cross-platform support
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        stop_loading("Public IP found")
        print(response.text)
    except requests.RequestException:
        stop_loading("Failed, trying fallback", success=False)
        # Fallback to curl
        run_command(["curl", "-s", "ifconfig.me"])
    
    wait_for_input(networking)


def port_scanning():
    """Scan ports on a target IP."""
    logo()
    print("Scans a target for open ports.")
    
    ip = sanitize_input(input("\nEnter IP address to scan: "))
    
    if not is_valid_ip(ip):
        print(f"{RED}Invalid IP address.{RESET}")
        wait_for_input(networking)
        return
    
    print(f"\n{RED}Scanning ports for {ip}...{RESET}\n")
    run_command(["sudo", "nmap", "-sS", "-sV", "-O", ip])
    
    wait_for_input(networking)


def live_packet_capture():
    """Capture network packets in real-time."""
    logo()
    print("Captures and analyzes network traffic in real-time.")
    
    interface = sanitize_input(input(f"{GREEN}Enter interface (e.g., eth0, eth1): {RESET}"))
    
    if not interface:
        print("No interface specified.")
        wait_for_input(networking)
        return
    
    if not is_interface_up(interface):
        print(f"Interface {interface} appears to be down.")
        wait_for_input(networking)
        return
    
    print(f"\nStarting packet capture on {interface}")
    print(f"Press {GREEN}Ctrl+C{RESET} to stop\n")
    
    try:
        process = subprocess.Popen(["tshark", "-i", interface, "-P"])
        process.wait()
    except KeyboardInterrupt:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pcap_file = f"capture_{interface}_{current_time}.pcap"
        print(f"\nCapture stopped. File: {pcap_file}")
        if process:
            process.terminate()
            process.wait()
    except FileNotFoundError:
        print(f"{RED}tshark not found. Install wireshark/tshark.{RESET}")
    
    wait_for_input(networking)


def vuln_scan():
    """Run vulnerability scan using nmap."""
    logo()
    print(f"{RED}Vulnerability Scanning{RESET}")
    print("Scans a target to identify vulnerabilities.")
    print(f"{RED}{BOLD}This scan can take up to 30 minutes.{RESET}\n")
    
    target = sanitize_input(input("Enter target IP: "))
    
    if not is_valid_ip(target):
        print(f"{RED}Invalid IP address.{RESET}")
        wait_for_input(networking)
        return
    
    print("Scanning for vulnerabilities...\n")
    run_command(["sudo", "nmap", "--script", "vuln", target])
    
    wait_for_input(networking)
