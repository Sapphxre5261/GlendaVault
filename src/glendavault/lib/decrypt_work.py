import os
from cryptography.fernet import Fernet

def safe_decrypt_workflow(key, vault_file_path, output_folder):
    cipher = Fernet(key)
    
    # 1. เช็คว่ามีไฟล์ที่ถูกล็อกอยู่ใน Vault จริงไหม
    if not os.path.exists(vault_file_path):
        print("ไม่พบไฟล์ใน Vault!")
        return

    # 2. อ่านข้อมูลที่เข้ารหัสจาก Vault (อ่านแบบไบต์ rb)
    with open(vault_file_path, 'rb') as f:
        encrypted_data = f.read()
        
    # 3. ถอดรหัสข้อมูล
    try:
        decrypted_data = cipher.decrypt(encrypted_data)
    except Exception as e:
        print("ถอดรหัสไม่สำเร็จ! รหัสผ่านไม่ถูกต้อง หรือไฟล์เสียหาย")
        return

    # 4. ตั้งชื่อไฟล์ปลายทางสำหรับนำมาใช้งาน (เอา .locked ออก)
    base_filename = os.path.basename(vault_file_path)
    # ตัดคำว่า .locked ออกเพื่อให้กลับมาเป็นชื่อเดิม (สมมติว่าตอนเก็บเราเติม .locked)
    original_filename = base_filename.replace(".locked", "")
    
    output_path = os.path.join(output_folder, original_filename)
    
    # 5. เขียนไฟล์ปกติลงในโฟลเดอร์ทำงาน (เขียนแบบไบต์ wb)
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)
        
    print(f"-> ดึงไฟล์ออกจาก Vault และถอดรหัสสำเร็จ: {output_path}")
    print(f"-> (ไฟล์ต้นฉบับใน Vault ยังคงปลอดภัยอยู่ ไม่ได้ถูกลบ)")