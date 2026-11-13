import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from config import load_ini_config_salt

def gen_key_with_password(password,salt):
    # 2. สร้างสิ่งที่เรียกว่า "Salt" (เกลือ) ขึ้นมาสุ่ม 16 ไบต์
    # Salt มีไว้เพื่อป้องกันการแฮกด้วยวิธี Rainbow Table (ช่วยให้รหัสผ่านปลอดภัยขึ้นมาก)
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000, # จำนวนรอบในการคำนวณ เพื่อให้เดารหัสผ่านยากขึ้น
    )

    # แปลงกุญแจให้อยู่ในรูปแบบที่ Fernet (ระบบเข้ารหัส) ใช้งานได้
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    # print(f"\nรหัสผ่านที่คุณพิมพ์: {user_password}")
    print(f"กุญแจลับที่แปลงออกมาได้: {key}\n")

    return key



# password = input("Enter password : ")

# password_hash = gen_key_with_password(password)
# print('hash key = ',password_hash)
    