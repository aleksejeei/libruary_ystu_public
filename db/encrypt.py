from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib
import os
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

class AESCipher:
    def __init__(self, secret_key: str):
        if not secret_key:
            raise ValueError("Ключ шифрования не может быть пустым")
        self.key = hashlib.sha256(secret_key.encode()).digest()

    def encrypt(self, data: str) -> str:
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        return base64.b64encode(iv + encrypted).decode('ascii')

    def decrypt(self, enc_data: str) -> str:
        """Расшифровывает данные из base64-строки"""
        enc_data = base64.b64decode(enc_data)
        iv = enc_data[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(enc_data[16:]), AES.block_size)
        return decrypted.decode('utf-8')
