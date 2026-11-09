from cryptography.fernet import Fernet
from gen_key import gen_key_with_password

def encrypt_file(key, source_path, dest_path):
    # 1. นำ Key มาสร้างตัวเข้ารหัส/ถอดรหัส
    cipher = Fernet(key)
    
    # 2. เปิดอ่านไฟล์ต้นฉบับแบบไบต์ (rb = Read Binary)
    # วิธีนี้จะดึงข้อมูลดิบของไฟล์ทุกประเภทมาได้ครบถ้วน (ไม่ว่าจะเป็นรูป, PDF, หรือข้อความ)
    with open(source_path, 'rb') as f:
        original_data = f.read()
        
    # 3. ทำการเข้ารหัสข้อมูลไบต์นั้น
    encrypted_data = cipher.encrypt(original_data)
    
    # 4. บันทึกข้อมูลที่เข้ารหัสแล้วลงไฟล์ปลายทางแบบไบต์ (wb = Write Binary)
    with open(dest_path, 'wb') as f:
        f.write(encrypted_data)
        
    print(f"เข้ารหัสไฟล์สำเร็จ! บันทึกไว้ที่: {dest_path}")


print('start')
password = input("password : ")
hash = gen_key_with_password(password)

encrypt_file(hash,"test.txt","encrypt.sphx")


