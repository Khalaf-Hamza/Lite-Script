# Lite-Script - My Graduating Project
# EduPen AI - Educational Penetration Testing Tool

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-Educational-orange.svg)

**Created by Khalaf & Timaa**

EduPen AI is a comprehensive educational penetration testing toolkit with AI-powered vulnerability reporting. This tool is designed for authorized security testing and educational purposes only.

---

## 🚀 Features

### 1. Network Tools & Scanners
- View network interfaces
- Display and change MAC addresses (MAC spoofing)
- Host discovery on networks
- DNS lookup and enumeration
- Public IP address detection
- Port scanning with service detection
- Live packet capture
- Vulnerability scanning

### 2. Cryptography Tools
- Hash calculator (MD5, SHA-1, SHA-256, SHA-512)
- File encryption (Fernet symmetric encryption)
- File decryption

### 3. Exploit Tools
- Dictionary attacks (John the Ripper)
- DoS attacks (ICMP flood, SYN flood)
- WPA2 WiFi cracking
- Subdirectory discovery (Gobuster)

### 4. Extra Modules
- Email information gathering (Holehe)
- Service vulnerability finder (Metasploit integration)

### 5. Comprehensive AI-Powered Scanning
- Nuclei vulnerability scanning
- Shodan deep scanning
- VirusTotal malware detection
- Nmap port scanning
- Directory discovery
- SSL/TLS analysis
- HTTP security headers analysis
- DNS enumeration
- **AI-powered PDF report generation using Gemini 3 Pro**

---

## 📋 Requirements

### System Requirements
- **Operating System:** Linux (Kali Linux recommended), Windows (limited features)
- **Python:** 3.8 or higher
- **Root/Admin Access:** Required for many network and exploit features

### Required Python Packages
The tool will auto-install missing packages, but you can install them manually:

```bash
pip install --break-system-packages requests colorama pyfiglet bs4 cryptography netifaces reportlab shodan vt-py
```

Or using the requirements list:
- `requests` - HTTP library
- `colorama` - Terminal colors
- `pyfiglet` - ASCII art
- `bs4` (BeautifulSoup4) - HTML parsing
- `cryptography` - Encryption/decryption
- `netifaces` - Network interface info
- `reportlab` - PDF generation
- `shodan` - Shodan API client
- `vt-py` - VirusTotal API client

### Required External Tools (Linux)
The following tools are required for full functionality:

```bash
# On Debian/Ubuntu/Kali:
sudo apt-get update
sudo apt-get install -y gobuster nmap macchanger

# Python tools:
pip install holehe
```

Additional tools (optional but recommended):
- `john` (John the Ripper) - Password cracking
- `hping3` - Network packet crafting
- `tshark` (Wireshark) - Packet capture
- `msfconsole` (Metasploit) - Exploit framework
- `wifisky` - WiFi cracking

---

## 🔧 Installation

### Quick Start (Linux)

1. Clone or download the repository:
```bash
cd /path/to/edupen-ai
```

2. Make the main script executable:
```bash
chmod +x LiteScript_modular.py
```

3. Run the tool:
```bash
python3 LiteScript_modular.py
```

4. On first run (Linux only), the tool will offer to install itself system-wide:
```bash
# After installation, you can run from anywhere:
LiteScript
```

### Manual Installation

1. Install Python dependencies:
```bash
pip install --break-system-packages -r requirements.txt
```

2. Install system tools:
```bash
sudo apt-get install -y gobuster nmap macchanger
pip install holehe
```

3. Run the tool:
```bash
python3 LiteScript_modular.py
```

---

## 🎯 Usage

### Starting the Tool

```bash
python3 LiteScript_modular.py
```

### Main Menu Options

1. **Manual Tools** - Access individual security tools
   - Auxiliary (Network, Crypto)
   - Exploits
   - Extra Modules

2. **Comprehensive Scan (AI-Powered)** - Full automated security assessment with AI report

### Navigation
- Enter the number to select an option
- Press `Enter` to go back to the previous menu
- Type `%` to exit the program

---

## 📊 Comprehensive Scan (AI-Powered)

The comprehensive scan feature combines multiple security tools and generates a professional PDF report using AI analysis.

### Available Scan Types

**Cloud APIs (Run in Parallel):**
1. Nuclei - CVE and misconfiguration scanning
2. Shodan - Deep port and vulnerability scanning
3. VirusTotal - Malware and reputation checking

**Local Scans (Run Sequentially):**
4. Nmap - Active port scanning
5. Directory Discovery - Hidden path enumeration
6. SSL/TLS Analysis - Certificate validation
7. HTTP Headers - Security header analysis
8. DNS Enumeration - DNS record discovery

### Usage Example

```
Enter target (URL or IP): example.com
Select scans (e.g., 1+2+8 or 'all'): 1+2+8
```

The tool will:
1. Run selected scans in parallel (cloud) or sequentially (local)
2. Collect all vulnerability data
3. Send results to Gemini AI for analysis
4. Generate a professional PDF report with:
   - Executive summary
   - Key findings
   - Detailed analysis
   - Prioritized recommendations
   - Conclusion

---

## 🔑 API Keys Configuration

The tool uses several API services. Update the keys in `Config.py`:

```python
SHODAN_API_KEY = "your_shodan_key_here"
VIRUSTOTAL_API_KEY = "your_virustotal_key_here"
NUCLEI_TOKEN = "your_nuclei_token_here"
GEMINI_API_KEY = "your_gemini_key_here"
```

### Getting API Keys

- **Shodan:** https://account.shodan.io/
- **VirusTotal:** https://www.virustotal.com/gui/my-apikey
- **Nuclei:** Contact Nuclei API provider
- **Gemini:** https://makersuite.google.com/app/apikey

---

## 📁 Project Structure

```
edupen-ai/
├── LiteScript_modular.py    # Main entry point
├── Main.py                   # Main menu and initialization
├── Config.py                 # Configuration and API keys
├── Network.py                # Network tools
├── Crypto.py                 # Cryptography tools
├── Exploit.py                # Exploit tools
├── Extra.py                  # Extra modules
├── Scanner.py                # Comprehensive scanning & AI reporting
├── Ui.py                     # UI components (logo, menus)
├── Utils.py                  # Utility functions
├── Loading.py                # Loading animations
├── __init__.py               # Package initialization
└── README.md                 # This file
```

---

## 🛠️ Troubleshooting

### Common Issues

**1. "Command not found" errors**
- Install the required external tools (see Requirements section)
- Ensure tools are in your system PATH

**2. Permission denied errors**
- Many features require root/sudo access
- Run with: `sudo python3 LiteScript_modular.py`

**3. API errors (403, rate limits)**
- Check your API keys in Config.py
- Shodan free tier has limited queries
- Wait before retrying if rate-limited

**4. Import errors**
- Install missing Python packages: `pip install package_name`
- Use `--break-system-packages` flag on Kali Linux

**5. Windows compatibility**
- Some features are Linux-only (MAC changing, certain exploits)
- Run in WSL (Windows Subsystem for Linux) for full functionality

---

## 🎓 Educational Use Cases

This tool is designed for:
- Learning penetration testing concepts
- Practicing ethical hacking skills
- Understanding network security
- Authorized security assessments
- Capture The Flag (CTF) competitions
- Security research in controlled environments

---

## 🔒 Security Best Practices

When using this tool:
1. Always get written permission before testing
2. Use in isolated lab environments when learning
3. Never test production systems without authorization
4. Keep API keys secure and never commit them to public repos
5. Follow responsible disclosure for any vulnerabilities found
6. Understand the legal implications in your jurisdiction

---

## 📝 Example Workflows

### Network Reconnaissance
```
1. Select "Manual Tools"
2. Choose "Auxiliary (Network, Crypto)"
3. Select "Network Tools"
4. Run "Host Discovery" to find active hosts
5. Run "Port Scanning" on discovered hosts
6. Analyze results
```

### Full Security Assessment
```
1. Select "Comprehensive Scan (AI-Powered)"
2. Enter target URL or IP
3. Select 'all' for complete scan
4. Wait for scans to complete
5. Review generated PDF report
```

### File Encryption
```
1. Select "Manual Tools"
2. Choose "Auxiliary (Network, Crypto)"
3. Select "Cryptography Tools"
4. Choose "Encrypt a file"
5. Provide file path
6. Save the generated .key file securely
```

---

## 🤝 Contributing

This is an educational project. If you'd like to contribute:
- Report bugs or issues
- Suggest new features
- Improve documentation
- Add new security modules

---

## 📜 License

This tool is provided for educational purposes only. Use responsibly and legally.

---

## 👥 Authors

**Khalaf & Timaa**

Created as an educational penetration testing toolkit with AI-powered reporting capabilities.

---

## 🙏 Acknowledgments

This tool integrates and leverages:
- Nmap - Network scanning
- Gobuster - Directory enumeration
- John the Ripper - Password cracking
- Shodan - Internet-wide scanning
- VirusTotal - Malware detection
- Nuclei - Vulnerability scanning
- Google Gemini AI - Report generation
- And many other open-source security tools

---

## 📞 Support

For educational support and questions:
- Review the documentation carefully
- Check troubleshooting section
- Ensure all requirements are installed
Contact Me On My Email : khalaf.hamza.email@gmail.com
