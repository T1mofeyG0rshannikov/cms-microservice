from functools import lru_cache

from cryptography.fernet import Fernet

# Генерация ключа
key = b"P6CFrx15uVDNlvJxer5KkZWRj_fyOPNIlW4dLqGA4OQ="
cipher = Fernet(key)


@lru_cache
def get_fernet_key():
    return 1, 1


class LinkEncryptor:
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def encrypt(self, string: str) -> str:
        message_bytes = string.encode("utf-8")
        # Шифрование
        encrypted_message = cipher.encrypt(message_bytes)
        return encrypted_message.decode("utf-8")

    def decrypt(self, string: str) -> str:
        decrypted_message = cipher.decrypt(string)
        # Преобразование байт обратно в строку
        return decrypted_message.decode("utf-8")


def get_link_encryptor():
    return LinkEncryptor(*get_fernet_key())
