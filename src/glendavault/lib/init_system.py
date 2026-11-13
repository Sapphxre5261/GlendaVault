import os
from pathlib import Path
import sqlite3
from cryptography.fernet import Fernet
from config import save_ini_config_salt, load_ini_config_salt
from gen_key import gen_key_with_password

BASE_DIR = Path(__file__).resolve().parent
# VAULT_DIR = BASE_DIR / "GL_Vault"
DB_PATH = VAULT_DIR / "vault.db"
CONFIG_PATH = VAULT_DIR / "config.ini"
WORK_SPACE = BASE_DIR / "work_space"

def init_vault(password: str):

    #สร้างและตั้งชื่อตู้เก็บไฟล์
    valut_name = input("Vault Name : ")
    VAULT_DIR = BASE_DIR / valut_name

    """
    ขั้นตอนที่ 1: ตรวจสอบและสร้าง Vault ครั้งแรก
    - สร้างโฟลเดอร์ GL_Vault
    - สร้าง Salt และเก็บใน config.ini
    - สร้างตารางใน SQLite (vault.db) สำหรับเก็บไฟล์ที่เข้ารหัส
    """
    print("กำลังตรวจสอบระบบ Vault...")
    
    # 1. สร้างโฟลเดอร์ Vault ถ้ายังไม่มี
    if not VAULT_DIR.is_dir():
        os.makedirs(VAULT_DIR)
        print(f"-> Create {VAULT_DIR} folder")

        # os.makedirs(WORK_SPACE) #สร้างโฟลเดอร์สำหรับเอาไหล์ที่ถอดรหัสกลับมาใช้งาน
        # print("-> Create work_space folder") 
                                                                                                        
        # สร้างและบันทึก Salt สำหรับรหัสผ่าน
        save_ini_config_salt(CONFIG_PATH)
        print("-> สร้างค่า Salt ลง config.ini สำเร็จ")
    else:
        print("-> พบโฟลเดอร์ Vault แล้ว")

    # 2. สร้างตาราง SQLite สำหรับเก็บข้อมูลไฟล์
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
                                                                                                                                                          
    # สร้างตารางชื่อ files
    # id: รหัสประจำไฟล์ (UUID)
    # encrypted_path: ชื่อ/เส้นทางไฟล์เดิมที่ถูกเข้ารหัสแล้ว
    # file_data: ข้อมูลเนื้อหาไฟล์ที่ถูกเข้ารหัสแล้ว (BLOB)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            encrypted_path TEXT NOT NULL,
            file_data BLOB NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("-> เตรียมฐานข้อมูล (vault.db) พร้อมใช้งานแล้ว!")
