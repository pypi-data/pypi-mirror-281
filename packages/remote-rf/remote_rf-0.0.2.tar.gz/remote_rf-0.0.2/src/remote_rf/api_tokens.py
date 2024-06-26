import os
import hashlib
import base64
import secrets
from dotenv import load_dotenv, set_key, find_dotenv

### API Token Management
# API Tokens are used to authenticate clients to the device
# API Tokens are stored locally on the device in its .env file

dotenv_path = find_dotenv('.env')
load_dotenv(dotenv_path)

def hash_token(token):
    salt = os.urandom(16)  # 16 bytes of random salt
    hashed = hashlib.sha256(salt + token.encode()).hexdigest()  # Hash to sha256 standard
    return salt.hex(), hashed

def validate_token(incoming_token):
    for key, value in os.environ.items():
        if key.startswith('TOKEN_'):
            salt, hash = value.split(':')
            if validate_internal_token(salt, hash, incoming_token):
                return True
    return False

def validate_internal_token(stored_salt, stored_hash, incoming_token):
    incoming_hash = hashlib.sha256(bytes.fromhex(stored_salt) + incoming_token.encode()).hexdigest()
    return incoming_hash == stored_hash

def generate_api_token(length=16):
    random_bytes = secrets.token_bytes(length)  # Generate a random byte string
    token = base64.urlsafe_b64encode(random_bytes).decode('utf-8')  # Encode the byte string in a URL-safe base64 format
    return token.rstrip('=')

def write_to_env(token):
    salt, hashed = hash_token(token)
    token_entry = f'{salt}:{hashed}'
    # Find the highest current TOKEN_n and increment
    token_key_prefix = "TOKEN_"
    count = 0
    for key in os.environ.keys():
        if key.startswith(token_key_prefix):
            count += 1
    set_key(dotenv_path, token_key_prefix + str(count), token_entry)
    load_dotenv()

# Example usage:
if __name__ == '__main__':
    new_token = generate_api_token()
    write_to_env(new_token)
    print(f'Generated new token: {new_token}')
    assert validate_token(new_token), "Token validation failed!"
    print("Token validation succeeded!")

