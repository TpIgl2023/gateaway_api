import hashlib
import secrets
import bcrypt

from Core.Environment.env import HASHING_SALT

def hashString(string):
    salt = HASHING_SALT.encode('utf-8')
    # Combine password and salt, then hash
    string_salt_combo = string.encode('utf-8') + salt
    hashed_string = hashlib.sha256(string_salt_combo).hexdigest()
    print(hashed_string)
    return hashed_string