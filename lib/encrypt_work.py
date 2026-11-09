import os
from cryptography.fernet import Fernet

def safe_encrypt_workflow(key, source_file_path, vault_folder):
    cipher = Fernet(key)
    
    # 1. เช็คว่ามีไฟล์ต้นฉบับจริงไหม
    if not os.path.exists(source_file_path):
        print("ไม่พบไฟล์ต้นฉบับ!")
        return

    # 2. อ่านไฟล์ต้นฉบับ
    with open(source_file_path, 'rb') as f:
        original_data = f.read()
        
    # 3. เข้ารหัสข้อมูล
    encrypted_data = cipher.encrypt(original_data)
    
    # 4. กำหนดชื่อไฟล์ปลายทางใน Vault (สร้างไฟล์ใหม่ใน Vault)
    filename = os.path.basename(source_file_path)
    vault_dest_path = os.path.join(vault_folder, filename + ".locked")
    
    # บันทึกไฟล์ใหม่ลง Vault
    with open(vault_dest_path, 'wb') as f:
        f.write(encrypted_data)
    print(f"-> สร้างไฟล์เข้ารหัสใหม่ใน Vault สำเร็จ: {vault_dest_path}")
    
    # 5. [สำคัญ] ลบไฟล์ต้นฉบับทิ้ง เพื่อไม่ให้มีข้อมูลดิบค้างอยู่ข้างนอกห้องนิรภัย
    os.remove(source_file_path)
    print(f"-> ลบไฟล์ต้นฉบับนอก Vault ทิ้งเรียบร้อย เพื่อความปลอดภัย")