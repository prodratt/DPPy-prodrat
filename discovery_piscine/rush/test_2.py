import sys
import tkinter as tk
from tkinter import messagebox

# ==========================================
# 1. DATA STRUCTURES (โครงสร้างข้อมูล)
# ==========================================
# dict: จัดเก็บข้อมูลโต๊ะ (ID, ประเภท, ความจุ, มีปลั๊กไฟไหม, สถานะ)
tables = {
    "T01": {"type": "Single", "capacity": 1, "has_plug": True, "status": "Available"},
    "T02": {"type": "Group", "capacity": 4, "has_plug": True, "status": "Available"},
    "T03": {"type": "Silent Zone", "capacity": 2, "has_plug": False, "status": "Available"},
    "T04": {"type": "Group", "capacity": 6, "has_plug": True, "status": "Available"},
    "T05": {"type": "Single", "capacity": 1, "has_plug": False, "status": "Available"}
}

# list: จัดเก็บประวัติรายการจอง
bookings = []
booking_counter = 100


# ==========================================
# BONUS: GUI POP-UP FUNCTIONS (Tkinter)
# ==========================================
def show_popup_info(title, message):
    """แสดง Pop-up แจ้งเตือนข้อมูลทั่วไป"""
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()

def show_popup_error(title, message):
    """แสดง Pop-up แจ้งเตือนข้อผิดพลาด"""
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()


# ==========================================
# CUSTOM FUNCTIONS & HELPER LOGIC
# ==========================================
def check_availability(table_id, tables_data):
    """
    Function 1 (Parameter + Return Value):
    ตรวจสอบว่าโต๊ะมีอยู่จริงและสถานะว่างหรือไม่
    """
    if table_id in tables_data:
        return tables_data[table_id]["status"] == "Available"
    return False

def view_all_tables():
    """แสดงรายการโต๊ะและสถานะทั้งหมด"""
    print("\n------------------------------------------------------------")
    print("                รายการโต๊ะอ่านหนังสือทั้งหมด                ")
    print("------------------------------------------------------------")
    print(f"{'รหัสโต๊ะ':<8} | {'ประเภท':<12} | {'ความจุ (คน)':<11} | {'ปลั๊กไฟ':<8} | {'สถานะ':<10}")
    print("-" * 60)
    for t_id, data in tables.items():
        plug_str = "มี" if data["has_plug"] else "ไม่มี"
        status_str = "🟢 ว่าง" if data["status"] == "Available" else "🔴 มีผู้ใช้"
        print(f"{t_id:<8} | {data['type']:<12} | {data['capacity']:<11} | {plug_str:<8} | {status_str:<10}")
    print("-" * 60)

def book_table():
    """
    Function 2: ดำเนินการจองโต๊ะ พร้อมระบบ Validation และ Business Rules
    """
    global booking_counter
    print("\n--- [เมนูที่ 1] จองโต๊ะอ่านหนังสือ ---")
    view_all_tables()
    
    table_id = input("\nกรอกรหัสโต๊ะที่ต้องการจอง (เช่น T01): ").strip().upper()
    
    # Input Validation: ตรวจสอบว่ามีรหัสโต๊ะในระบบหรือไม่
    if table_id not in tables:
        msg = f"ไม่พบรหัสโต๊ะ '{table_id}' ในระบบ!"
        print(f"❌ ข้อผิดพลาด: {msg}")
        show_popup_error("เกิดข้อผิดพลาด", msg)
        return

    # Rule 1: ป้องกันการจองซ้ำ (Table Availability)
    if not check_availability(table_id, tables):
        msg = f"โต๊ะ {table_id} ไม่ว่างในขณะนี้ (มีผู้ใช้งานอยู่)"
        print(f"❌ ปฏิเสธการจอง: {msg}")
        show_popup_error("การจองล้มเหลว", msg)
        return

    # Input Validation & Type Handling
    try:
        guests = int(input("กรอกจำนวนผู้ใช้งาน (คน): "))
        hours = int(input("กรอกจำนวนชั่วโมงที่ต้องการจอง (1-4 ชม.): "))
    except ValueError:
        msg = "กรุณากรอกตัวเลขจำนวนเต็มเท่านั้น!"
        print(f"❌ ข้อผิดพลาด: {msg}")
        show_popup_error("ข้อมูลไม่ถูกต้อง", msg)
        return

    # Input Validation: ห้ามใส่ค่าติดลบหรือ 0
    if guests <= 0 or hours <= 0:
        msg = "จำนวนคนและจำนวนชั่วโมงต้องมากกว่า 0!"
        print(f"❌ ปฏิเสธการจอง: {msg}")
        show_popup_error("ข้อมูลไม่ถูกต้อง", msg)
        return

    # Rule 2: ตรวจสอบจำนวนคนกับขนาดความจุของโต๊ะ (Capacity Check)
    if guests > tables[table_id]["capacity"]:
        msg = f"โต๊ะ {table_id} รองรับผู้ใช้งานได้สูงสุดเพียง {tables[table_id]['capacity']} คนเท่านั้น"
        print(f"❌ ปฏิเสธการจอง: {msg}")
        show_popup_error("ความจุเกินกำหนด", msg)
        return

    # Rule 3: จำกัดชั่วโมงการจองสูงสุดไม่เกิน 4 ชั่วโมง (Max Booking Limit)
    if hours > 4:
        msg = "อนุญาตให้จองโต๊ะได้สูงสุดไม่เกิน 4 ชั่วโมงต่อครั้ง"
        print(f"❌ ปฏิเสธการจอง: {msg}")
        show_popup_error("เกินจำกัดเวลา", msg)
        return

    student_name = input("กรอกชื่อผู้จอง: ").strip()
    if not student_name:
        msg = "ชื่อผู้จองต้องไม่อยู่ในลักษณะค่าว่าง!"
        print(f"❌ ข้อผิดพลาด: {msg}")
        show_popup_error("ข้อมูลไม่ถูกต้อง", msg)
        return

    # เมื่อผ่านเงื่อนไขทั้งหมด ทำการบันทึกข้อมูล
    booking_counter += 1
    tables[table_id]["status"] = "Occupied"
    
    booking_record = {
        "booking_id": booking_counter,
        "student_name": student_name,
        "table_id": table_id,
        "guests": guests,
        "hours": hours,
        "status": "Active"
    }
    bookings.append(booking_record)
    
    success_msg = f"จองสำเร็จ!\nรหัสการจอง: #{booking_counter}\nโต๊ะ: {table_id}\nผู้จอง: {student_name}"
    print(f"\n✅ {success_msg}")
    show_popup_info("การจองสำเร็จ", success_msg)

def cancel_booking():
    """ยกเลิกการจอง / คืนโต๊ะ"""
    print("\n--- [เมนูที่ 3] ยกเลิกการจอง / เช็กเอาต์คืนโต๊ะ ---")
    try:
        b_id = int(input("กรอกรหัสการจองที่ต้องการยกเลิก (เช่น 101): "))
    except ValueError:
        print("❌ ข้อผิดพลาด: กรุณากรอกรหัสการจองเป็นตัวเลข!")
        return

    # ค้นหารายการจอง
    found_booking = None
    for item in bookings:
        if item["booking_id"] == b_id and item["status"] == "Active":
            found_booking = item
            break

    if found_booking:
        found_booking["status"] = "Cancelled"
        t_id = found_booking["table_id"]
        tables[t_id]["status"] = "Available"
        
        msg = f"ยกเลิกการจอง #{b_id} (โต๊ะ {t_id}) เรียบร้อยแล้ว โต๊ะกลับมาว่างอีกครั้ง"
        print(f"✅ {msg}")
        show_popup_info("ยกเลิกสำเร็จ", msg)
    else:
        msg = f"ไม่พบรหัสการจอง #{b_id} ที่ใช้งานอยู่!"
        print(f"❌ ข้อผิดพลาด: {msg}")
        show_popup_error("ไม่พบข้อมูล", msg)

def search_and_summary():
    """
    Function 3 (Algorithm & Data Processing):
    1. Filtered Search: ค้นหาโต๊ะที่ว่างและมีปลั๊กไฟ
    2. Data Analytics: คำนวณอัตราการใช้งานโต๊ะทั้งหมด (%)
    """
    print("\n--- [เมนูที่ 4] ค้นหาและสรุปสถิติข้อมูล ---")
    
    # Algorithm 1: ค้นหาโต๊ะที่ว่าง AND มีปลั๊กไฟ (Filtered Search)
    print("\n🔍 1. โต๊ะที่ว่างและมีปลั๊กไฟ (Suitable for Laptops):")
    plug_available_count = 0
    for t_id, data in tables.items():
        if data["has_plug"] and data["status"] == "Available":
            print(f"   - โต๊ะ {t_id} [{data['type']}] | รองรับ: {data['capacity']} คน")
            plug_available_count += 1
            
    if plug_available_count == 0:
        print("   (ไม่มีโต๊ะที่มีปลั๊กไฟว่างในขณะนี้)")

    # Algorithm 2: คำนวณเปอร์เซ็นต์อัตราการใช้งานโต๊ะ (Occupancy Rate Analytics)
    total_tables = len(tables)
    occupied_tables = sum(1 for t in tables.values() if t["status"] == "Occupied")
    occupancy_rate = (occupied_tables / total_tables) * 100 if total_tables > 0 else 0

    total_active_hours = sum(b["hours"] for b in bookings if b["status"] == "Active")

    print("\n📊 2. สรุปภาพรวมสถิติการใช้งานระบบ:")
    print(f"   • โต๊ะทั้งหมดในระบบ: {total_tables} ตัว")
    print(f"   • โต๊ะที่มีผู้ใช้งานอยู่: {occupied_tables} ตัว")
    print(f"   • อัตราการใช้งาน (Occupancy Rate): {occupancy_rate:.1f}%")
    print(f"   • การจองที่ active ทั้งหมด: {len([b for b in bookings if b['status'] == 'Active'])} รายการ")
    print(f"   • ชั่วโมงการใช้งานสะสมรวม: {total_active_hours} ชั่วโมง")


# ==========================================
# MAIN APPLICATION LOOP
# ==========================================
def main():
    """ฟังก์ชันหลักสำหรับรันโปรแกรมและแสดง Menu Loop"""
    while True:
        print("\n==================================================")
        print("    ระบบจองโต๊ะอ่านหนังสือ (STUDY SPACE SYSTEM)   ")
        print("==================================================")
        print("1. จองโต๊ะอ่านหนังสือ (Book a Table)")
        print("2. ดูรายการโต๊ะและสถานะทั้งหมด (View Tables)")
        print("3. ยกเลิกการจอง / คืนโต๊ะ (Cancel Booking)")
        print("4. ค้นหาโต๊ะตามเงื่อนไข & สรุปสถิติ (Search & Analytics)")
        print("5. ออกจากระบบ (Exit)")
        print("==================================================")
        
        choice = input("เลือกเมนูที่ต้องการ (1-5): ").strip()

        if choice == "1":
            book_table()
        elif choice == "2":
            view_all_tables()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            search_and_summary()
        elif choice == "5":
            print("\nขอบคุณที่ใช้บริการระบบจองโต๊ะอ่านหนังสือ Goodbye!")
            sys.exit(0)
        else:
            print("❌ ตัวเลือกไม่ถูกต้อง! กรุณากรอกตัวเลขตั้งแต่ 1 ถึง 5")

if __name__ == "__main__":
    main()