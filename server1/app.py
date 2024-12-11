from flask import Flask, request, jsonify
import requests
import bcrypt
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) # Allow CORS requests

DATABASE_PATH = 'database.csv'  # Ensure this file is present or mounted

@app.route('/api/hash_password', methods=['POST'])
def hash_and_forward():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password must be provided'}), 400

    username = data['username']
    password = data['password']

    # Check if the username already exists
    if os.path.exists(DATABASE_PATH):
        with open(DATABASE_PATH, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) == 3:
                    db_username = parts[0]
                    if db_username == username:
                        # Username already exists
                        return jsonify({'message': 'Sign up failed: username already taken'}), 400

    hashed, salt = hash_password(password)
    print("Server1 (signup): Hashed Password:", hashed.decode('utf-8'))

    try:
        server2_url = 'http://server2:5001/api/receive_hash'
        response = requests.post(server2_url, json={'hash': hashed.decode('utf-8')})
        response_data = response.json()

        encrypted_hash = response_data.get('encrypted_hash', None)
        print("Server1 (signup): Response from Server2:", response_data)

        # Append username, salt, and encrypted_hash to database.csv
        with open(DATABASE_PATH, 'a') as f:
            f.write(f"{username},{salt.decode('utf-8')},{encrypted_hash}\n")

        return jsonify({
            'message': 'Sign up successful',
            'username': username,
            'original_password': password,
            'hashed_password': hashed.decode('utf-8'),
            'encrypted_hash': encrypted_hash
        })

    except Exception as e:
        print("Server1 (signup): Error reaching Server2:", str(e))
        return jsonify({'error': f'Failed to reach server2: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password must be provided'}), 400

    username = data['username']
    password = data['password']

    if not os.path.exists(DATABASE_PATH):
        return jsonify({'error': 'No database file found'}), 500

    user_found = False
    user_salt = None
    user_encrypted_hash = None

    with open(DATABASE_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 3:
                continue
            db_username, db_salt, db_encrypted_hash = parts
            if db_username == username:
                user_found = True
                user_salt = db_salt.encode('utf-8')  # salt stored as string, need bytes
                user_encrypted_hash = db_encrypted_hash
                break

    if not user_found:
        return jsonify({'error': 'Username not found in the database'}), 400

    hashed_login = hash_password_login(password, user_salt)
    hashed_login_str = hashed_login.decode('utf-8')

    try:
        server2_url = 'http://server2:5001/api/decrypt_hash'
        response = requests.post(server2_url, json={'encrypted_hash': user_encrypted_hash})
        response_data = response.json()

        decrypted_hash = response_data.get('decrypted_hash', None)
        if decrypted_hash is None:
            return jsonify({'error': 'Failed to decrypt hash from server2'}), 500

        if decrypted_hash == hashed_login_str:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Login failed: password does not match'}), 401

    except Exception as e:
        print("Server1 (login): Error reaching Server2:", str(e))
        return jsonify({'error': f'Failed to reach server2: {str(e)}'}), 500

def hash_password(password: str) -> tuple:
    """Hash the password with bcrypt and generate a salt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed, salt

def hash_password_login(password: str, salt: bytes) -> bytes:
    """Hash the password using the provided salt."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

if __name__ == '__main__':
    # Assuming that server1 runs on port 5002
    app.run(host='0.0.0.0', port=5002)
