from config import RED, GREEN, YELLOW, BLUE, BOLD, RESET
try:
    import pyfiglet
except ImportError:
    pyfiglet = None

def logo():
    """Display the application logo."""
    if pyfiglet:
        uline = pyfiglet.figlet_format("---------")
        print(f'{YELLOW}{uline}{RESET}')
        title = pyfiglet.figlet_format("EDUPEN AI")
        print(f'{RED}{title}{RESET}')
        print(f'{YELLOW}{uline}{RESET}')
    else:
        print(f'{YELLOW}-----------------{RESET}')
        print(f'{RED}   EDUPEN AI   {RESET}')
        print(f'{YELLOW}-----------------{RESET}')
        
    print(f"{BLUE}{BOLD}[---]\t\tEduPen AI\t\t[---]{RESET}")
    print(f"{BLUE}{BOLD}[---]\tCreated By Khalaf & Timaa \t[---]{RESET}")
    print(f"{GREEN}{BOLD}\t(--Welcome to EduPen AI--)\n{RESET}")


def print_menu_header(title):
    """Print a formatted menu header."""
    print(f"\n{RED}----------------{RESET} {GREEN}{title}{RESET} {RED}----------------{RESET}")


def print_menu_option(number, text):
    """Print a formatted menu option."""
    print(f"{RED}{number}){RESET} {GREEN}{text}{RESET}")
