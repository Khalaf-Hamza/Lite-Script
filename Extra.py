import re
import threading
from config import RED, GREEN, YELLOW, BOLD, RESET
from utils import (
    run_command, sanitize_input, wait_for_input, handle_menu_choice,
    threaded_loading_animation, set_loading
)
from ui import logo, print_menu_header, print_menu_option

def extra_modules_menu():
    """Extra modules menu."""
    from main import main_menu
    
    logo()
    print_menu_header("Extra Modules")
    print_menu_option("1", "Email Information Gathering")
    print_menu_option("2", "Service Vulnerability Finder")

    option = input("=> ")

    menu_actions = {
        "1": email_info_gather,
        "2": service_vulnerability_finder,
    }

    if option in menu_actions:
        menu_actions[option]()
    elif not handle_menu_choice(option, main_menu):
        print("Invalid option.")
        extra_modules_menu()


def email_info_gather():
    """Gather information about an email address."""
    logo()
    print(f"{GREEN}Email information gathering using holehe.{RESET}")
    print("Finds sites where an email is registered.")
    print(f"{RED}Note: Results may not be 100% accurate.{RESET}\n")
    
    email = input(f"{RED}{BOLD}Enter email address: {RESET}").strip()
    
    if not email or '@' not in email:
        print("Invalid email address.")
        wait_for_input(extra_modules_menu)
        return
    
    email = sanitize_input(email)
    
    result = run_command(["holehe", email], capture_output=True)
    
    if result and result.stdout:
        print(f"{GREEN}Registered sites found:{RESET}")
        for line in result.stdout.splitlines():
            if '[+]' in line:
                print(f"{YELLOW}{line}{RESET}")
    else:
        print(f"{RED}No results or holehe not installed.{RESET}")
    
    wait_for_input(extra_modules_menu)


def service_vulnerability_finder():
    """Search for exploits in Metasploit."""
    
    logo()
    print(f"{GREEN}Search for exploits in Metasploit Framework.{RESET}")
    
    service_name = input(f"{GREEN}Enter service name (e.g., ssh): {RESET}").strip()
    service_version = input(f"{GREEN}Enter version (optional): {RESET}").strip()
    
    if not service_name:
        print("No service specified.")
        wait_for_input(extra_modules_menu)
        return
    
    service_name = sanitize_input(service_name)
    service_version = sanitize_input(service_version)
    
    search_query = service_name
    if service_version:
        search_query += f" {service_version}"

    # Start loading animation in thread
    set_loading(True)
    t = threading.Thread(target=threaded_loading_animation)
    t.start()

    # Search in Metasploit
    result = run_command(
        ['msfconsole', '-q', '-x', f'search name:{search_query}; exit'],
        capture_output=True
    )
    
    set_loading(False)
    t.join()

    if not result or not result.stdout:
        print("No results or msfconsole not available.")
        wait_for_input(extra_modules_menu)
        return

    print("\nSearch Results:")
    print(result.stdout)

    # Parse exploits from output
    exploits = []
    for line in result.stdout.splitlines():
        if re.search(r'^\s*\d+\s+exploit/', line):
            exploits.append(line.strip())

    if not exploits:
        print("No exploits found.")
        wait_for_input(extra_modules_menu)
        return

    print("\nAvailable Exploits:")
    for i, exploit in enumerate(exploits, 1):
        print(f"{i}: {exploit}")

    try:
        choice = int(input("\nChoose exploit number (0 to cancel): ")) - 1
        if choice < 0 or choice >= len(exploits):
            print("Cancelled.")
            wait_for_input(extra_modules_menu)
            return
        
        chosen_exploit = exploits[choice].split()[1]
        print(f"\nSelected: {chosen_exploit}")
        
        # Show options
        opt_result = run_command(
            ['msfconsole', '-q', '-x', f'use {chosen_exploit}; show options; exit'],
            capture_output=True
        )
        
        if opt_result and opt_result.stdout:
            print("\nExploit Options:")
            print(opt_result.stdout)
        
    except (ValueError, IndexError):
        print("Invalid selection.")
    
    wait_for_input(extra_modules_menu)
