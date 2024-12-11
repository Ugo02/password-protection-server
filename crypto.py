from flask import Flask, request, jsonify
import tink
from tink import aead
from tink import cleartext_keyset_handle
from tink import JsonKeysetReader
import bcrypt
import base64

#%% Server 1 : Hash function
def hash_password(password: str) -> tuple:
    """Hash the password with bcrypt and generate a salt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt) 
    """encode() transforms a string to bytes"""
    return hashed, salt

#%% Server 2 : Initializing Tink for AEAD

# Register AEAD primitive with Tink
aead.register()

# Loading the protection key (master_key_aead)
MASTER_KEY_PATH = "master_key.json"
with open(MASTER_KEY_PATH, "r") as master_key_file:
    master_key_data = master_key_file.read()  # Read the raw content of the file
    master_key_handle = cleartext_keyset_handle.read(JsonKeysetReader(master_key_data))

# The key to decrypt the keyset is in the master_key.json file. It is wrapped in master_key_handle after being read and processed by Tink.

# Convert the master key to an AEAD primitive
master_key_aead = master_key_handle.primitive(aead.Aead)  # Creating the AEAD primitive

# Loading the protected keyset
KEYSET_PATH = "encrypted_keyset.json"
with open(KEYSET_PATH, "r") as keyset_file:
    keyset_data = keyset_file.read()  # Read the raw content of the file
    keyset_handle = tink.KeysetHandle.read(JsonKeysetReader(keyset_data), master_key_aead)

# Creating the AEAD primitive
aead_primitive = keyset_handle.primitive(aead.Aead)

# Encrypt a hash using AEAD
def encrypt_hash(hash):
    ciphertext = aead_primitive.encrypt(hash, associated_data=b"metadata")
    return base64.b64encode(ciphertext).decode('utf-8')

#_____________________________________________________

# Function to decrypt the hash
def decrypt_hash(encrypted_hash: str) -> str:
    """Decrypt a hash encrypted with AEAD."""
    # Convert the base64-encoded hash to bytes
    ciphertext = base64.b64decode(encrypted_hash)
    # Decrypt using AEAD
    decrypted_bytes = aead_primitive.decrypt(ciphertext, associated_data=b"metadata")
    # Convert the bytes back to a string and return it
    return decrypted_bytes.decode('utf-8')

#%% Server 1 : Main function
def main():
    # Step 1: Collecting user input
    user_name = input("Enter the username: ")
    password = input("Enter the password: ")

    # Step 2: Hash the password
    hashed, salt = hash_password(password)
    print(hashed)

    # Step 3: Encrypt the hash
    encrypted_hash = encrypt_hash(hashed)
    print(f"Encrypted hash: {encrypted_hash}")

    # Step 4: Decrypt the hash
    decrypted_hash = decrypt_hash(encrypted_hash)
    print(f"Decrypted hash: {decrypted_hash}")

if _name_ == '_main_':
    main()