from flask import Flask, request, jsonify
import base64
import tink
from tink import aead
from tink import JsonKeysetReader
from tink.cleartext_keyset_handle import read as cleartext_read

app = Flask(__name__)

#%% Server 2 : Initializing Tink for AEAD
aead.register()

# Loading the master key
MASTER_KEY_PATH = "master_key.json"
with open(MASTER_KEY_PATH, "r") as master_key_file:
    master_key_data = master_key_file.read()
    master_key_handle = cleartext_read(JsonKeysetReader(master_key_data))

# Convert the master key to an AEAD primitive
master_key_aead = master_key_handle.primitive(aead.Aead)

# Load the protected keyset
KEYSET_PATH = "encrypted_keyset.json"
with open(KEYSET_PATH, "r") as keyset_file:
    keyset_data = keyset_file.read()
    keyset_handle = tink.KeysetHandle.read(JsonKeysetReader(keyset_data), master_key_aead)

# Creating the AEAD primitive from the keyset
aead_primitive = keyset_handle.primitive(aead.Aead)

def encrypt_hash(hash_str: str) -> str:
    ciphertext = aead_primitive.encrypt(hash_str.encode('utf-8'), associated_data=b"metadata")
    return base64.b64encode(ciphertext).decode('utf-8')

def decrypt_hash(encrypted_hash: str) -> str:
    ciphertext = base64.b64decode(encrypted_hash)
    decrypted_bytes = aead_primitive.decrypt(ciphertext, associated_data=b"metadata")
    return decrypted_bytes.decode('utf-8') 

@app.route('/api/receive_hash', methods=['POST'])
def receive_and_encrypt():
    data = request.get_json()
    if not data or 'hash' not in data:
        print("Server2: Invalid data received, missing 'hash'.")
        return jsonify({'error': 'Hash not provided'}), 400

    received_hash = data['hash']
    # Print received data for debugging
    print("Server2: Received hash:", received_hash)

    # Encrypt the hash
    encrypted_hash = encrypt_hash(received_hash)
    print("Server2: Encrypted hash:", encrypted_hash)

    return jsonify({
        'message': 'Hash received and encrypted successfully',
        'encrypted_hash': encrypted_hash
    })

@app.route('/api/decrypt_hash', methods=['POST'])
def decrypt_and_return():
    data = request.get_json()
    if not data or 'encrypted_hash' not in data:
        print("Server2: Invalid data received, missing 'encrypted_hash'.")
        return jsonify({'error': 'Encrypted hash not provided'}), 400

    encrypted_hash = data['encrypted_hash']
    print("Server2: Received encrypted_hash for decryption:", encrypted_hash)

    try:
        decrypted = decrypt_hash(encrypted_hash)
        print("Server2: Decrypted hash:", decrypted)
        return jsonify({
            'message': 'Encrypted hash decrypted successfully',
            'decrypted_hash': decrypted
        })
    except Exception as e:
        print("Server2: Decryption error:", e)
        return jsonify({'error': 'Decryption failed'}), 500

if __name__ == '__main__':
    # Server2 listens on port 5001
    app.run(host='0.0.0.0', port=5001)
