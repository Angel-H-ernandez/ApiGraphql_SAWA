# core/encryption_helper.py
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.signing import Signer

class EncryptionHelper:
    def __init__(self):
        self.cipher_suite = Fernet(settings.ENCRYPTION_KEY)
        self.signer = Signer()

    def encrypt_data(self, data):
        if not data:
            return None
        return self.cipher_suite.encrypt(str(data).encode()).decode()

    def decrypt_data(self, encrypted_data):
        if not encrypted_data:
            return None
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()