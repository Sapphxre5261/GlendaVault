import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class VaultManager:
    def __init__(self, password: str, salt: bytes = None):
        # ถ้าไม่มี salt (เช่น สร้าง Vault ใหม่) ให้สุ่มขึ้นมา 16 ไบต์
        if salt is None:
            self.salt = os.urandom(16)
        else:
            self.salt = salt
        
        # แปลง Password เป็น Key เข้ารหัสด้วย PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)

    def encrypt_filename(self, filename: str) -> str:
        """เข้ารหัสชื่อไฟล์ เพื่อซ่อนชื่อจริงไม่ให้คนอื่นรู้บน Cloud"""
        encrypted_bytes = self.cipher.encrypt(filename.encode())
        return base64.urlsafe_b64encode(encrypted_bytes).decode().rstrip("=")

    def decrypt_filename(self, encrypted_filename: str) -> str:
        """ถอดรหัสชื่อไฟล์กลับมาเป็นชื่อเดิม"""
        padding = '=' * (-len(encrypted_filename) % 4)
        decoded_bytes = base64.urlsafe_b64decode(encrypted_filename + padding)
        return self.cipher.decrypt(decoded_bytes).decode()

    def encrypt_file(self, source_path: str, dest_path: str):
        """อ่านไฟล์ต้นฉบับมาเข้ารหัส และบันทึกเก็บไว้"""
        with open(source_path, 'rb') as f:
            data = f.read()
        encrypted_data = self.cipher.encrypt(data)
        with open(dest_path, 'wb') as f:
            f.write(encrypted_data)

    def decrypt_file(self, source_path: str, dest_path: str):
        """อ่านไฟล์ที่เข้ารหัสมาถอดรหัส และบันทึกเป็นไฟล์ปกติ"""
        with open(source_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = self.cipher.decrypt(encrypted_data)
        with open(dest_path, 'wb') as f:
            f.write(decrypted_data)