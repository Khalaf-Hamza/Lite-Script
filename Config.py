
# =============================================================================
# CONFIGURATION
# =============================================================================

REQUIRED_TOOLS = [
    ('gobuster', 'sudo apt-get install -y gobuster'),
    ('nmap', 'sudo apt-get install -y nmap'),
    ('holehe', 'pip install holehe'),
    ('macchanger', 'sudo apt-get install -y macchanger'),
]

REQUIRED_PACKAGES = [
    'requests',
    'colorama',
    'pyfiglet',
    'bs4',
    'cryptography',
    'netifaces',
    'reportlab',
    'shodan',
    'vt-py',
]

INSTALL_NAME = "LiteScript"
INSTALL_PATH = f"/usr/local/bin/{INSTALL_NAME}"

# ANSI color codes for cleaner code
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

# API Keys (Ideally these should be environment variables, but keeping as is for now)
SHODAN_API_KEY = "CdfpVQOuLEfDghL7oVnU4pS5CMy4KwAu"
VIRUSTOTAL_API_KEY = "e75856df7bc86cef599368dc7b6b52bbdfba92c29b87f4b0ca373de5ddd405e5"
NUCLEI_TOKEN = "1018"
GEMINI_API_KEY = "AIzaSyD8_HMYv6vWA__rxmxeUfWMlDxhPuWaP_g"
GEMINI_MODEL = "gemini-3-pro-preview"
