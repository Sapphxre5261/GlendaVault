import configparser
import base64
import os

# ini_filename = "lib/vault_config.ini"

# --- ส่วนที่ 1: บันทึกข้อมูลลงไฟล์ .ini ---
def save_ini_config_salt(file_name):
    # 1. สุ่ม Salt เหมือนเดิม
    raw_salt = os.urandom(32)
    salt_str = base64.b64encode(raw_salt).decode('utf-8')
    
    # 2. เรียกใช้งาน configparser
    config = configparser.ConfigParser()
    
    # 3. กำหนดหมวดหมู่ (Section) และค่าที่จะเก็บ
    config['Settings'] = {
        'salt': salt_str
    }
    
    # 4. เขียนลงไฟล์ .ini
    with open(file_name, 'w', encoding='utf-8') as f:
        config.write(f)
        
    print("บันทึกไฟล์ .ini สำเร็จ!")
    print(f"ค่า Salt ที่แปลงแล้ว: {salt_str}\n")

# --- ส่วนที่ 2: อ่านข้อมูลกลับมาจากไฟล์ .ini ---
def load_ini_config_salt(file_name):
    if not os.path.exists(file_name):
        print("ยังไม่มีไฟล์ .ini กรุณาสร้างก่อน")
        return None

    config = configparser.ConfigParser()
    config.read(file_name, encoding='utf-8')
    
    # ดึงค่า salt จากหมวดหมู่ [Settings]
    salt_str = config['Settings']['salt']
    
    # แปลงกลับเป็น Bytes เพื่อเอาไปใช้สร้างกุญแจ
    raw_salt = base64.b64decode(salt_str.encode('utf-8'))
    
    print("อ่านไฟล์ .ini สำเร็จ!")
    print(f"โหลด Salt กลับมาเป็น Bytes ได้แล้ว: {raw_salt}")
    return raw_salt

# --- ทดลองรัน ---
# if __name__ == "__main__":
#     # จำลองการสร้างไฟล์ .ini ครั้งแรก
#     save_ini_config()
    
#     # เปิดหน้าตาไฟล์ .ini ที่ถูกสร้างขึ้นมาให้ดูคร่าวๆ
#     print("--- หน้าตาข้างในไฟล์ vault_config.ini ---")
#     with open(ini_filename, 'r', encoding='utf-8') as f:
#         print(f.read())
#     print("---------------------------------------")
    
#     # จำลองการเปิดโปรแกรมรอบใหม่แล้วอ่านค่า
#     print("--- จำลองการอ่านค่ารอบใหม่ ---")
#     loaded_salt = load_ini_config()