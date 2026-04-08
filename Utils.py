import sys
import subprocess
import importlib.util
import os
import glob
import time
import itertools
import threading
import re
import datetime
from config import RED, GREEN, YELLOW, RESET, INSTALL_PATH, INSTALL_NAME, REQUIRED_TOOLS, REQUIRED_PACKAGES
from loading import start_loading, stop_loading, with_loading, quick_loading, progress_bar

# Global flag for loading animation (kept for backward compatibility)
loading = False

def set_loading(value):
    global loading
    loading = value

def get_loading():
    return loading

# Auto-install missing packages function
def auto_install_package(package_name, import_name=None):
    """Auto-install a missing package using pip with --break-system-packages for Kali."""
    if import_name is None:
        import_name = package_name
    print(f"📦 Installing {package_name}...")
    try:
        # Try with --break-system-packages first (for Kali/Debian)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", package_name],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            # Fallback to regular pip install
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q", package_name],
                capture_output=True, text=True
            )
        if result.returncode == 0:
            print(f"✅ {package_name} installed successfully!")
            # Refresh import system
            importlib.invalidate_caches()
            return True
        print(f"❌ Failed to install {package_name}: {result.stderr}")
        return False
    except Exception as e:
        print(f"❌ Error installing {package_name}: {e}")
        return False

def safe_import(module_name, package_name=None, from_list=None):
    """Safely import a module, installing if necessary."""
    if package_name is None:
        package_name = module_name
    
    try:
        if from_list:
            mod = __import__(module_name, fromlist=from_list)
            return mod
        else:
            return __import__(module_name)
    except ImportError:
        auto_install_package(package_name)
        importlib.invalidate_caches()
        # Re-run the script after installation
        print("🔄 Restarting script with new packages...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

def is_linux():
    """Check if running on Linux."""
    return sys.platform.startswith('linux')

def is_installed():
    """Check if script is installed system-wide."""
    if not is_linux():
        return True  # Skip installation check on non-Linux
    return os.path.isfile(INSTALL_PATH) and os.access(INSTALL_PATH, os.X_OK)

def install_script():
    """Install script to system path (Linux only)."""
    import shutil
    if not is_linux():
        print(f"{YELLOW}Installation is only supported on Linux.{RESET}")
        return
    
    # Need to be careful here with __file__ in a package
    # In this refactored version, we might need to copy the whole folder or a specific runner.
    # For now, we'll assume this function might need adjustment if deployed as a package.
    # We'll use sys.argv[0] to find the entry script.
    current_path = os.path.realpath(sys.argv[0])
    
    # Ask for sudo if not root
    if os.geteuid() != 0:
        print("🔐 Installation requires root permission. Asking for sudo...")
        subprocess.call(['sudo', sys.executable, *sys.argv])
        sys.exit()

    shutil.copy(current_path, INSTALL_PATH)
    os.chmod(INSTALL_PATH, 0o755)
    print(f"✅ Installed successfully! You can now run the tool using: {INSTALL_NAME}")
    sys.exit()

def check_and_install_tools():
    """Check for required external tools and offer to install missing ones."""
    if not is_linux():
        print(f"{YELLOW}Tool installation check skipped (non-Linux system).{RESET}")
        return
    
    missing_tools = []
    for tool, install_cmd in REQUIRED_TOOLS:
        result = subprocess.run(['which', tool], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            missing_tools.append((tool, install_cmd))
    
    if missing_tools:
        print(f"Missing tools: {', '.join(tool for tool, _ in missing_tools)}")
        user_input = input("Install them now? (yes/no): ").strip().lower()
        if user_input in ['yes', 'y']:
            for tool, install_cmd in missing_tools:
                try:
                    print(f"Installing {tool}...")
                    # Use list form to avoid shell injection
                    subprocess.check_call(install_cmd.split())
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install {tool}. Please install manually.")
                    print(f"Error: {e}")
        else:
            print("Some features may not work without required tools.")

def check_and_install_packages():
    """Check for required Python packages and offer to install missing ones."""
    missing_packages = []
    
    for package in REQUIRED_PACKAGES:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        user_input = input("Install them now? (yes/no): ").strip().lower()
        if user_input in ['yes', 'y']:
            for package in missing_packages:
                try:
                    # Try with --break-system-packages first (for Kali/Debian)
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", "--break-system-packages", package],
                        capture_output=True, text=True
                    )
                    if result.returncode != 0:
                        # Fallback to regular pip install
                        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    print(f"✅ {package} installed")
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to install {package}")
        else:
            print("Some features may not work without required packages.")

try:
    import netifaces
except ImportError:
    netifaces = None

def is_interface_up(interface):
    """Check if a network interface is up and has an IP address."""
    if netifaces is None:
        return True  # Assume up if we can't check
    try:
        return netifaces.AF_INET in netifaces.ifaddresses(interface)
    except (ValueError, KeyError):
        return False

try:
    import readline
except ImportError:
    readline = None

def input_file_path(prompt):
    """Get file path input with tab completion support."""
    if readline is not None:
        def complete(text, state):
            matches = glob.glob(text + '*') + [None]
            return matches[state]
        
        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(complete)
    
    return input(prompt)

def simple_loading_animation(message="Loading", style="dots"):
    """Display a cool loading animation (non-threaded, fixed duration)."""
    quick_loading(message=message, duration=1.5, style=style)

def threaded_loading_animation(message="Searching, please wait"):
    """Display a spinner animation (for use with threading)."""
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if not loading:
            break
        sys.stdout.write(f'\r{message}... {c}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rComplete!                              \n')


def cool_loading(message="Processing", style="cyber"):
    """Start a cool threaded loading animation.
    
    Styles available: cyber, matrix, pulse, blocks, dots, hack, wave
    
    Usage:
        start_loading("Scanning target", "hack")
        # ... do work ...
        stop_loading("Scan complete!")
    """
    start_loading(message, style)


def finish_loading(message="Done!"):
    """Stop the loading animation with a completion message."""
    stop_loading(message)

def is_valid_ip(ip):
    """Validate IPv4 address format."""
    if not ip:
        return False
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    # Check each octet is 0-255
    octets = ip.split('.')
    return all(0 <= int(octet) <= 255 for octet in octets)

def is_valid_subnet(subnet):
    """Validate subnet format (e.g., 192.168.0.0/24)."""
    if '/' not in subnet:
        return is_valid_ip(subnet)
    ip_part, cidr = subnet.rsplit('/', 1)
    if not is_valid_ip(ip_part):
        return False
    try:
        cidr_int = int(cidr)
        return 0 <= cidr_int <= 32
    except ValueError:
        return False

def is_valid_port(port):
    """Validate port number."""
    try:
        port_number = int(port)
        return 0 <= port_number <= 65535
    except (ValueError, TypeError):
        return False

def is_valid_file_path(path):
    """Check if file path exists."""
    return os.path.exists(path) if path else False

def sanitize_input(user_input, allowed_chars=None):
    """Basic input sanitization to prevent command injection."""
    if not user_input:
        return ""
    # Remove potentially dangerous characters
    dangerous_chars = [';', '|', '&', '$', '`', '(', ')', '{', '}', '[', ']', '<', '>', '\n', '\r']
    result = user_input
    for char in dangerous_chars:
        result = result.replace(char, '')
    return result.strip()

def run_command(cmd_list, capture_output=False):
    """Safely run a command using list form (no shell injection)."""
    try:
        if capture_output:
            result = subprocess.run(cmd_list, capture_output=True, text=True)
            return result
        else:
            subprocess.run(cmd_list)
            return None
    except FileNotFoundError:
        print(f"{RED}Command not found: {cmd_list[0]}{RESET}")
        return None
    except subprocess.SubprocessError as e:
        print(f"{RED}Command failed: {e}{RESET}")
        return None

def handle_menu_choice(choice, back_func=None, exit_msg="Exiting Lite Script. Goodbye!"):
    """Handle common menu navigation choices."""
    if choice == "":
        if back_func:
            back_func()
        return True
    elif choice == "%":
        print(exit_msg)
        sys.exit(0)
    return False

def wait_for_input(back_func=None):
    """Wait for user input to continue or exit."""
    while True:
        choice = input(f"\n{GREEN}Press Enter to go back or '%' to exit: {RESET}")
        if choice == "":
            if back_func:
                back_func()
            return
        elif choice == "%":
            print("Exiting Lite Script. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Press Enter or %.")
