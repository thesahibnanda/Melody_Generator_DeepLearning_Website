import secrets
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import urlsafe_b64encode, urlsafe_b64decode
import hashlib
import os

DB_Name = "sqlite.db"

def db_exists(db_path=DB_Name):
    return os.path.exists(db_path)

def generate_random_key(length):
    return secrets.token_bytes(length)

KEY = generate_random_key(16)

def encrypt(plaintext, key=KEY):
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)
    
    # Create an AES cipher object with the provided key and IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    
    # Create an encryptor object
    encryptor = cipher.encryptor()
    
    # Encrypt the plaintext
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    
    # Combine the IV and ciphertext and encode in base64
    encrypted_message = urlsafe_b64encode(iv + ciphertext).decode()
    
    return encrypted_message

def decrypt(encrypted_message, key=KEY):
    # Decode the base64 string
    decoded_message = urlsafe_b64decode(encrypted_message.encode())
    
    # Extract the IV and ciphertext
    iv = decoded_message[:16]
    ciphertext = decoded_message[16:]
    
    # Create an AES cipher object with the provided key and IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    
    # Create a decryptor object
    decryptor = cipher.decryptor()
    
    # Decrypt the ciphertext
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Use 'replace' to handle decoding errors
    return decrypted_text.decode('utf-8', 'replace')


# Create Database
def createDB(file_name=DB_Name, content=""):
    try:
        file = open(file_name, 'w')
        file.write(content)
        file.close()
    except Exception as e:
        return e

# Hash Password
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

# Add User As CSV And Encrypt And Then To Text File
def add_user(name, email, password, path=DB_Name):
    # Check if DB exists, if not, create one
    if not db_exists():
        createDB()

    # Open the file in read and write mode
    with open(path, 'r+') as file:
        file_content = file.read()

        if file_content == "":
            decrypted_data = ""
        else:
            decrypted_data = decrypt(file_content)

        # Append user data with a newline character
        decrypted_data += f'{email},{name},{hash_password(password)}\n'
        encrypted_data = encrypt(decrypted_data)

        # Move the file cursor to the beginning, write the encrypted data, and truncate the file
        file.seek(0)
        file.write(encrypted_data)
        file.truncate()

def check_user_existence(email, file_path=DB_Name):
    if not db_exists(file_path):
        return False  # Database file does not exist

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

            if file_content == "":
                return False  # Database is empty, user does not exist

            decrypted_data = decrypt(file_content)
            users = decrypted_data.split('\n')

            for user_info in users:
                if user_info:
                    user_email = user_info.split(',')[0]
                    if user_email == email:
                        return True  # User exists in the database

        return False  # User does not exist in the database
    except Exception as e:
        return False


def is_password_correct(email, password, file_path=DB_Name):
    if not db_exists(file_path):
        return False  # Database file does not exist

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

            if file_content == "":
                return False  # Database is empty, user does not exist

            decrypted_data = decrypt(file_content)
            users = decrypted_data.split('\n')

            for user_info in users:
                if user_info:
                    user_email, _, hashed_password = user_info.split(',')
                    if user_email == email:
                        # Check if the provided password matches the stored hashed password
                        return hash_password(password) == hashed_password

        return False  # User does not exist in the database
    except Exception as e:
        return False

def change_password(email, new_password, file_path=DB_Name):
    if not db_exists(file_path):
        return False  # Database file does not exist.
    if not check_user_existence(email):
        return False

    try:
        with open(file_path, 'r+') as file:
            file_content = file.read()

            if file_content == "":
                return False  # Database is empty, user does not exist.

            decrypted_data = decrypt(file_content)
            users = decrypted_data.split('\n')

            updated_data = ""

            for user_info in users:
                if user_info:
                    user_email, name, hashed_password = user_info.split(',')
                    if user_email == email:
                        # Update the hashed password with the new password
                        hashed_new_password = hash_password(new_password)
                        updated_data += f'{user_email},{name},{hashed_new_password}\n'
                    else:
                        updated_data += f'{user_email},{name},{hashed_password}\n'

            # Encrypt the updated data
            encrypted_data = encrypt(updated_data)

            # Move the file cursor to the beginning, write the encrypted data, and truncate the file
            file.seek(0)
            file.write(encrypted_data)
            file.truncate()

            return True  # Password changed successfully.

    except Exception as e:
        return e  # Error changing password


