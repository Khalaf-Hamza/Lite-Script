import hashlib
import os
from Config import RED, GREEN, YELLOW, BOLD, RESET
from Utils import (
    safe_import, is_valid_file_path, input_file_path, wait_for_input, 
    handle_menu_choice
)
from Ui import logo, print_menu_header, print_menu_option

try:
    from cryptography.fernet import Fernet
except ImportError:
    safe_import("cryptography")
    from cryptography.fernet import Fernet

def cryptography_menu():
    """Cryptography tools menu."""
    from main import auxop
    
    print_menu_header("Cryptography Tools")
    print_menu_option("1", "Hash Calculator")
    print_menu_option("2", "Encrypt a file")
    print_menu_option("3", "Decrypt a file")

    option = input(f"{GREEN}Select an option or Enter to go back, '%' to exit: {RESET}")

    menu_actions = {
        "1": hash_calculator,
        "2": encrypt_file,
        "3": decrypt_file,
    }

    if option in menu_actions:
        menu_actions[option]()
    elif not handle_menu_choice(option, auxop):
        print("Invalid option.")
        cryptography_menu()


def hash_calculator():
    """Calculate hash of a file."""
    logo()
    print("Computes a hash value for a given file.")
    print(f"\n{GREEN}Available Hash Algorithms:{RESET}")
    print_menu_option("1", "MD5")
    print_menu_option("2", "SHA-1")
    print_menu_option("3", "SHA-256")
    print_menu_option("4", "SHA-512")
    print_menu_option("0", "Return to previous menu")

    hash_type = input(f"{GREEN}Select hash type: {RESET}")

    if hash_type == "0":
        cryptography_menu()
        return

    hash_algorithms = {
        "1": hashlib.md5,
        "2": hashlib.sha1,
        "3": hashlib.sha256,
        "4": hashlib.sha512,
    }

    if hash_type not in hash_algorithms:
        print("Invalid hash type.")
        hash_calculator()
        return

    file_path = input_file_path("Enter path to file: ")
    
    if not file_path:
        hash_calculator()
        return
    
    if not is_valid_file_path(file_path):
        print(f"{RED}File not found.{RESET}")
        wait_for_input(cryptography_menu)
        return

    try:
        hash_obj = hash_algorithms[hash_type]()
        with open(file_path, "rb") as f:
            # Read in chunks for large files
            for chunk in iter(lambda: f.read(8192), b""):
                hash_obj.update(chunk)
        print(f"\n{GREEN}Hash Result: {hash_obj.hexdigest()}{RESET}")
    except IOError as e:
        print(f"{RED}Error reading file: {e}{RESET}")
    
    wait_for_input(cryptography_menu)


def encrypt_file():
    """Encrypt a file using Fernet symmetric encryption."""
    logo()
    print("Encrypt a file using symmetric encryption.")
    
    file_path = input_file_path(f"{BOLD}Enter path of file to encrypt: {RESET}")
    
    if not file_path or not is_valid_file_path(file_path):
        print(f"{RED}File not found.{RESET}")
        wait_for_input(cryptography_menu)
        return

    try:
        # Generate key
        key = Fernet.generate_key()
        key_file = f"{file_path}.key"
        
        with open(key_file, "wb") as kf:
            kf.write(key)

        # Read and encrypt
        with open(file_path, "rb") as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)

        # Save encrypted file
        encrypted_path = f"{file_path}.encrypted"
        with open(encrypted_path, "wb") as ef:
            ef.write(encrypted_data)

        print(f"{GREEN}File encrypted: {encrypted_path}{RESET}")
        print(f"{YELLOW}Key saved to: {key_file}{RESET}")
        print(f"{RED}Keep the key file safe - you need it to decrypt!{RESET}")
        
    except IOError as e:
        print(f"{RED}Error: {e}{RESET}")
    
    wait_for_input(cryptography_menu)


def decrypt_file():
    """Decrypt a file using Fernet symmetric encryption."""
    logo()
    print("Decrypt a file using symmetric encryption.")
    
    encrypted_path = input_file_path(f"{BOLD}Enter path of encrypted file: {RESET}")
    
    if not encrypted_path or not is_valid_file_path(encrypted_path):
        print(f"{RED}Encrypted file not found.{RESET}")
        wait_for_input(cryptography_menu)
        return
    
    key_path = input_file_path(f"{BOLD}Enter path to key file: {RESET}")
    
    if not key_path or not is_valid_file_path(key_path):
        print(f"{RED}Key file not found.{RESET}")
        wait_for_input(cryptography_menu)
        return

    try:
        # Read key
        with open(key_path, "rb") as kf:
            key = kf.read()

        fernet = Fernet(key)

        # Read and decrypt
        with open(encrypted_path, "rb") as ef:
            encrypted_data = ef.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        # Save decrypted file
        decrypted_path = encrypted_path.replace(".encrypted", ".decrypted")
        with open(decrypted_path, "wb") as df:
            df.write(decrypted_data)

        print(f"{GREEN}File decrypted: {decrypted_path}{RESET}")
        
    except Exception as e:
        print(f"{RED}Decryption failed: {e}{RESET}")
    
    wait_for_input(cryptography_menu)
