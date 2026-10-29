# main.py

tables = {
    "T01": {"type": "Single", "capacity": 1, "has_plug": True, "status": "Available"},
    "T02": {"type": "Group", "capacity": 4, "has_plug": True, "status": "Available"},
    "T03": {"type": "Silent", "capacity": 2, "has_plug": False, "status": "Available"}
}

bookings = []
booking_counter = 100

def check_availability(table_id, tables_data):
    """ส่งคืน True ถ้าโต๊ะมีอยู่จริงและว่าง"""
    if table_id in tables_data:
        return tables_data[table_id]["status"] == "Available"
    return False

def book_table():
    global booking_counter
    print("\n--- จองโต๊ะอ่านหนังสือ ---")
    table_id = input("กรอกรหัสโต๊ะ (เช่น T01): ").strip().upper()
    
    # Validation 1: มีโต๊ะนี้หรือไม่ และ ว่างหรือไม่
    if not check_availability(table_id, tables):
        print("❌ ปฏิเสธการจอง: ไม่พบรหัสโต๊ะ หรือ โต๊ะไม่ว่าง!")
        return

    try:
        guests = int(input("จำนวนผู้ใช้งาน (คน): "))
        hours = int(input("จำนวนชั่วโมงที่ต้องการจอง (1-4 ชม.): "))
    except ValueError:
        print("❌ ข้อผิดพลาด: กรุณากรอกตัวเลขเท่านั้น!")
        return

    # Rule 1: ตรวจสอบความจุโต๊ะ
    if guests > tables[table_id]["capacity"]:
        print(f"❌ ปฏิเสธการจอง: โต๊ะนี้รองรับได้สูงสุด {tables[table_id]['capacity']} คน")
        return

    # Rule 2: ตรวจสอบจำนวนชั่วโมงสูงสุด
    if hours < 1 or hours > 4:
        print("❌ ปฏิเสธการจอง: สามารถจองได้ครั้งละ 1 - 4 ชั่วโมงเท่านั้น")
        return

    # บันทึกการจอง
    booking_counter += 1
    tables[table_id]["status"] = "Occupied"
    name = input("ชื่อผู้จอง: ").strip()
    
    booking_info = {
        "id": booking_counter,
        "name": name,
        "table": table_id,
        "hours": hours,
        "guests": guests
    }
    bookings.append(booking_info)
    print(f"✅ จองสำเร็จ! รหัสการจองของคุณคือ #{booking_counter}")

def main():
    while True:
        print("\n===== STUDY SPACE RESERVATION =====")
        print("1. จองโต๊ะอ่านหนังสือ")
        print("2. ดูสถานะโต๊ะทั้งหมด")
        print("3. ค้นหาโต๊ะที่มีปลั๊กไฟ")
        print("4. สรุปภาพรวมสถิติ")
        print("5. ออกจากระบบ")
        
        choice = input("เลือกเมนู (1-5): ").strip()
        
        if choice == "1":
            book_table()
        elif choice == "2":
            print("\n--- รายการโต๊ะทั้งหมด ---")
            for t_id, data in tables.items():
                print(f"โต๊ะ {t_id} | ประเภท: {data['type']} | ปลั๊ก: {data['has_plug']} | ความจุ: {data['capacity']} คน | สถานะ: {data['status']}")
        elif choice == "3":
            # Algorithm: ค้นหาโต๊ะที่มีปลั๊กและว่าง
            print("\n--- โต๊ะที่ว่างและมีปลั๊กไฟ ---")
            found = False
            for t_id, data in tables.items():
                if data["has_plug"] and data["status"] == "Available":
                    print(f"- โต๊ะ {t_id} ({data['type']}) รองรับได้ {data['capacity']} คน")
                    found = True
            if not found:
                print("ไม่มีโต๊ะที่มีปลั๊กไฟว่างในขณะนี้")
        elif choice == "4":
            # Algorithm: คำนวณเปอร์เซ็นต์การใช้งาน
            total = len(tables)
            occupied = sum(1 for t in tables.values() if t["status"] == "Occupied")
            rate = (occupied / total) * 100 if total > 0 else 0
            print(f"\n--- สรุปภาพรวม ---")
            print(f"โต๊ะทั้งหมด: {total} | ถูกใช้งาน: {occupied} | อัตราการใช้งาน: {rate:.1f}%")
            print(f"การจองทั้งหมดในระบบ: {len(bookings)} รายการ")
        elif choice == "5":
            print("ขอบคุณที่ใช้บริการ Goodbye!")
            break
        else:
            print("❌ เลือกเมนูไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")

if __name__ == "__main__":
    main()