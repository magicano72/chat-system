from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(secret):
    return base64.urlsafe_b64encode(hashlib.sha256(secret.encode()).digest())

def encrypt_image(image_bytes, secret):
    key = generate_key(secret)
    f = Fernet(key)
    return f.encrypt(image_bytes)

def decrypt_image(encrypted_bytes, secret):
    key = generate_key(secret)
    f = Fernet(key)
    return f.decrypt(encrypted_bytes)
