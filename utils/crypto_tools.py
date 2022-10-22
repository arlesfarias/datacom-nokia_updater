import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from os import urandom


def encrypt(content, password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode('utf-8'),
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
    f = Fernet(key)
    encrypted_content = f.encrypt(bytes(content, 'utf-8'))

    return encrypted_content.decode('utf-8')


def decrypt(encrypted_content, password, salt):
    encrypted_content = bytes(encrypted_content, 'utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode('utf-8'),
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
    f = Fernet(key)

    return f.decrypt(encrypted_content).decode('utf-8')


def generate_salt():
    return base64.urlsafe_b64encode(urandom(32)).decode('utf-8')
