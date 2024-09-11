from functools import lru_cache

from cryptography.fernet import Fernet


@lru_cache
def get_fernet_key():
    return Fernet.generate_key()


class LinkEncryptor:
    def __init__(self):
        self.fernet = Fernet(get_fernet_key())

    def encrypt(self, string: str) -> str:
        enc_string = self.fernet.encrypt(string.encode())
        return enc_string.decode()

    def decrypt(self, string: str) -> str:
        return self.fernet.decrypt(string.encode()).decode()
