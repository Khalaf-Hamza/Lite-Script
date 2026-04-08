import sys
from config import GREEN, BOLD, RESET, RED
from ui import logo, print_menu_header, print_menu_option
from utils import (
    check_and_install_packages, check_and_install_tools, 
    is_linux, is_installed, install_script
)
from network import networking
from crypto import cryptography_menu
from exploit import exploits_menu
from extra import extra_modules_menu
from scanner import nuclei_scan

def auxop():
    """Auxiliary options menu."""
    while True:
        logo()
        print_menu_header("Auxiliary Options")
        print(f"{GREEN}Press Enter to go back, '%' to exit{RESET}")
        print_menu_option("1", "Network Tools And Scanners")
        print_menu_option("2", "Cryptography Tools")
        
        option = input("=> ")
        
        if option == '1':
            networking()
        elif option == '2':
            cryptography_menu()
        elif option == '%':
            print("Exiting Lite Script. Goodbye!")
            sys.exit(0)
        elif option == '':
            main_menu()
            return
        else:
            print("Invalid option.")


def manual_tools_menu():
    """Manual tools selection menu."""
    while True:
        logo()
        print_menu_header("Manual Tools")
        print(f"{GREEN}Press Enter to go back, '%' to exit{RESET}")
        print_menu_option("1", "Auxiliary (Network, Crypto)")
        print_menu_option("2", "Exploits")
        print_menu_option("3", "Extra Modules")
        
        option = input(f"{GREEN}Select category or '%' to exit: {RESET}")
        
        if option == "1":
            auxop()
        elif option == "2":
            exploits_menu()
        elif option == "3":
            extra_modules_menu()
        elif option == "%":
            print("Exiting Lite Script. Goodbye!")
            sys.exit(0)
        elif option == "":
            main_menu()
            return
        else:
            print("Invalid option.")


def main_menu():
    """Main application menu."""
    while True:
        logo()
        print(f"\n{GREEN}{BOLD}Choose Options:{RESET}")
        print_menu_option("1", "Manual Tools")
        print_menu_option("2", "Comprehensive Scan (AI-Powered)")
        
        option = input(f"{GREEN}Select category or '%' to exit: {RESET}")
        
        if option == "1":
            manual_tools_menu()
        elif option == "2":
            nuclei_scan()
        elif option == "%":
            print("Exiting Lite Script. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option.")


def main():
    """Application entry point."""
    # Check dependencies
    check_and_install_packages()
    check_and_install_tools()
    
    # Install if first run (Linux only)
    if is_linux() and not is_installed():
        print("🛠️ First run detected. Installing to /usr/local/bin...")
        install_script()
    
    print("🚀 Running LiteScript...")
    main_menu()

if __name__ == "__main__":
    main()
