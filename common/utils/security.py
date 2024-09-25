from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os


def derive_key_from_password(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_data(data, password):
    salt = os.urandom(16)
    key = derive_key_from_password(password, salt)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode('utf-8'))
    return base64.urlsafe_b64encode(salt + encrypted_data).decode('utf-8')


def decrypt_data(encoded_encrypted_data, password):
    encrypted_data = base64.urlsafe_b64decode(encoded_encrypted_data.encode('utf-8'))
    salt = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    key = derive_key_from_password(password, salt)
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data
