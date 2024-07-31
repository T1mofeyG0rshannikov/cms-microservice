from cryptography.fernet import Fernet

key = Fernet.generate_key()


class LinkEncryptor:
    def __init__(self):
        self.fernet = Fernet(key)

    def encrypt(self, string: str) -> str:
        enc_string = self.fernet.encrypt(string.encode())
        return enc_string.decode()

    def decrypt(self, string: str) -> str:
        return self.fernet.decrypt(string.encode()).decode()
