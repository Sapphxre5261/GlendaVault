from cryptography.fernet import Fernet
from gen_key import gen_key_with_password

def decrypt_file(key, encrypted_path, output_path):
    # 1. นำ Key มาสร้างตัวถอดรหัส
    cipher = Fernet(key)
    
    # 2. เปิดอ่านไฟล์ที่ถูกเข้ารหัสแบบไบต์ (rb = Read Binary)
    with open(encrypted_path, 'rb') as f:
        encrypted_data = f.read()
        
    # 3. ทำการถอดรหัส (จะได้ข้อมูล bytes ดิบๆ กลับคืนมา)
    decrypted_data = cipher.decrypt(encrypted_data)
    
    # 4. บันทึกข้อมูลไบต์นั้นลงไฟล์ปลายทางแบบไบต์ (wb = Write Binary)
    # วิธีนี้จะทำให้ไฟล์กลับมาสมบูรณ์ 100% ไม่ว่าจะเป็นข้อความ รูปภาพ หรือ PDF
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)
        
    print(f"ถอดรหัสไฟล์สำเร็จ! กู้ไฟล์กลับมาที่: {output_path}")


password = input('password : ')

key = gen_key_with_password(password)

decrypt_file(key,'encrypt.sphx','decrypt.txt')