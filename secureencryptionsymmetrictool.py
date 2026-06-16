from cryptography.fernet import Fernet
import base64
import hashlib
import subprocess
import logging
from datetime import datetime
import getpass


logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ID : { encrypted_data, key_hash }
store = {}
id_counter = 1


print(" Secure Symmetric Encryption Tool ")
print("Type 'help' to see commands")


def generate_key_from_password(password):
    hash_key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hash_key)

while True:
    user_input = input("\n> ").strip()

    
    if user_input == "help":
        print("\nAvailable Commands:")
        print("encrypt <message/command>")
        print("decrypt <ID>")
        print("list")
        print("exit")

    
    elif user_input == "exit":
        print("Exiting tool...")
        logging.info("Tool exited by user")
        break

    
    elif user_input == "list":
        if not store:
            print("No stored encrypted items")
        else:
            print("Stored IDs:")
            for i in store:
                print(i)

   
    elif user_input.startswith("encrypt "):
        message = user_input[8:].strip()

        if not message:
            print("Message cannot be empty")
            continue

        password = getpass.getpass("Enter encryption key (password): ")

        key = generate_key_from_password(password)
        cipher = Fernet(key)

        encrypted_data = cipher.encrypt(message.encode())

        msg_id = f"ID{id_counter}"
        store[msg_id] = {
            "data": encrypted_data,
            "key_hash": hashlib.sha256(password.encode()).hexdigest()
        }
        id_counter += 1

        print("\nPlain Text:")
        print(message)

        print("\nEncrypted Data:")
        print(encrypted_data)

        print("\nStored as:", msg_id)

        logging.info(f"{msg_id} encrypted and stored")

   
    elif user_input.startswith("decrypt "):
        msg_id = user_input[8:].strip()

        if msg_id not in store:
            print("Invalid ID")
            continue

        password = getpass.getpass("Enter decryption key: ")


        entered_hash = hashlib.sha256(password.encode()).hexdigest()
        stored_hash = store[msg_id]["key_hash"]

        if entered_hash != stored_hash:
            print("❌ Wrong key! Decryption failed.")
            logging.warning(f"{msg_id} decryption failed (wrong key)")
            continue

        key = generate_key_from_password(password)
        cipher = Fernet(key)

        encrypted_data = store[msg_id]["data"]

        try:
            decrypted_message = cipher.decrypt(encrypted_data).decode()
        except:
            print("Decryption error")
            continue

        print("\nDecrypted Text:")
        print(decrypted_message)

        
        output = subprocess.getoutput(decrypted_message)

        if output and "not recognized" not in output.lower():
            print("\nCommand Output:")
            print(output)
            logging.info(f"{msg_id} decrypted and command executed")
        else:
            print("\nMessage Output:")
            print(decrypted_message)
            logging.info(f"{msg_id} decrypted as message")

   
    else:
        print("Invalid command. Type 'help'")

