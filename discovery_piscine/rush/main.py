import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# 1. DATA STRUCTURES & GLOBAL STATE
# ==========================================
tables = {
    "T01": {"type": "Single", "capacity": 1, "has_plug": True, "status": "Occupied"},
    "T02": {"type": "Group", "capacity": 4, "has_plug": True, "status": "Available"},
    "T03": {"type": "Silent Zone", "capacity": 2, "has_plug": False, "status": "Available"},
    "T04": {"type": "Group", "capacity": 6, "has_plug": True, "status": "Available"},
    "T05": {"type": "Single", "capacity": 1, "has_plug": False, "status": "Available"}
}

bookings = []
booking_counter = 100

# ==========================================
# 2. CORE FUNCTIONS & BUSINESS LOGIC
# ==========================================
def check_availability(table_id, tables_data):
    """Check if table exists and is available."""
    if table_id in tables_data:
        return tables_data[table_id]["status"] == "Available"
    return False

def refresh_table_view(table_widget):
    """Updates the custom table view, coloring ONLY the status column."""
    table_widget.config(state="normal")
    table_widget.delete("1.0", tk.END)

    # Table Header
    header = f"{'ID':^10}{'Type':^18}{'Capacity':^12}{'Plug':^10}{'Status':^12}\n"
    header_separator = "-" * 62 + "\n"
    
    table_widget.insert(tk.END, header, "header")
    table_widget.insert(tk.END, header_separator, "normal")

    # Table Rows
    for t_id, data in tables.items():
        plug_str = "Yes" if data["has_plug"] else "No"
        status_str = data["status"]

        table_widget.insert(tk.END, f"{t_id:^10}{data['type']:^18}{data['capacity']:^12}{plug_str:^10}", "normal")
        table_widget.insert(tk.END, f"{status_str:^12}\n", status_str)

    table_widget.config(state="disabled")

def book_table_action(entry_table, entry_name, entry_guests, entry_hours, table_widget):
    """Validates inputs and records a booking."""
    global booking_counter
    table_id = entry_table.get().strip().upper()
    student_name = entry_name.get().strip()
    guests_str = entry_guests.get().strip()
    hours_str = entry_hours.get().strip()

    if not table_id or not student_name or not guests_str or not hours_str:
        messagebox.showerror("Error", "All fields are required!")
        return

    if table_id not in tables:
        messagebox.showerror("Error", f"Table code '{table_id}' does not exist!")
        return

    if not check_availability(table_id, tables):
        messagebox.showerror("Booking Failed", f"Table {table_id} is currently occupied.")
        return

    try:
        guests = int(guests_str)
        hours = int(hours_str)
    except ValueError:
        messagebox.showerror("Error", "Guests and Hours must be positive whole numbers.")
        return

    if guests <= 0 or hours <= 0:
        messagebox.showerror("Error", "Guests and Hours must be greater than 0.")
        return

    if guests > tables[table_id]["capacity"]:
        messagebox.showerror("Capacity Exceeded", 
                             f"Table {table_id} max capacity is {tables[table_id]['capacity']} guests.")
        return

    if hours > 4:
        messagebox.showerror("Duration Limit", "Maximum allowed booking time is 4 hours.")
        return

    booking_counter += 1
    tables[table_id]["status"] = "Occupied"
    
    bookings.append({
        "booking_id": booking_counter,
        "student_name": student_name,
        "table_id": table_id,
        "guests": guests,
        "hours": hours,
        "status": "Active"
    })
    
    refresh_table_view(table_widget)
    messagebox.showinfo("Success", f"Booking Confirmed!\nBooking ID: #{booking_counter}\nTable: {table_id}")

    entry_table.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_guests.delete(0, tk.END)
    entry_hours.delete(0, tk.END)

def cancel_booking_action(entry_cancel_id, table_widget):
    """Cancels an active booking."""
    b_id_str = entry_cancel_id.get().strip()
    try:
        b_id = int(b_id_str)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric Booking ID.")
        return

    found = False
    for item in bookings:
        if item["booking_id"] == b_id and item["status"] == "Active":
            item["status"] = "Cancelled"
            tables[item["table_id"]]["status"] = "Available"
            found = True
            break

    if found:
        refresh_table_view(table_widget)
        messagebox.showinfo("Success", f"Booking #{b_id} has been cancelled.")
        entry_cancel_id.delete(0, tk.END)
    else:
        messagebox.showerror("Error", f"Active Booking ID #{b_id} not found.")

def show_analytics():
    """Algorithm: Filtered Search & Occupancy Stats."""
    plug_tables = [t for t, d in tables.items() if d["has_plug"] and d["status"] == "Available"]
    plug_str = ", ".join(plug_tables) if plug_tables else "None available"

    total = len(tables)
    occupied = sum(1 for t in tables.values() if t["status"] == "Occupied")
    rate = (occupied / total) * 100 if total > 0 else 0
    active_count = len([b for b in bookings if b['status'] == 'Active'])

    stats_msg = (
        f"🔍 Available Power Plug Tables: {plug_str}\n\n"
        f"📊 Analytics Summary:\n"
        f"• Total Tables: {total}\n"
        f"• Occupied Tables: {occupied}\n"
        f"• Occupancy Rate: {rate:.1f}%\n"
        f"• Active Bookings: {active_count}"
    )
    messagebox.showinfo("Search & Analytics", stats_msg)

# ==========================================
# 3. GUI LAYOUT & MAIN WINDOW
# ==========================================
def main():
    root = tk.Tk()
    root.title("Study Table Reservation System")
    root.minsize(650, 550)
    root.resizable(True, True)

    title_label = tk.Label(root, text="STUDY TABLE RESERVATION SYSTEM", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # --- Custom Table View ---
    table_frame = tk.Frame(root, bd=1, relief="solid")
    table_frame.pack(pady=10, padx=20, fill="x")

    table_widget = tk.Text(
        table_frame, 
        height=7, 
        width=65, 
        font=("Courier", 10, "bold"), 
        bg="white", 
        fg="black", 
        relief="flat"
    )
    table_widget.pack(fill="x", padx=5, pady=5)

    # Configure precise colors for text tags
    table_widget.tag_configure("header", foreground="black", font=("Courier", 10, "bold"))
    table_widget.tag_configure("normal", foreground="black")
    table_widget.tag_configure("Available", foreground="green")
    table_widget.tag_configure("Occupied", foreground="red")

    refresh_table_view(table_widget)

    # --- Booking Form Frame ---
    form_frame = tk.LabelFrame(root, text=" Reserve Table ", font=("Helvetica", 10, "bold"), padx=10, pady=10)
    form_frame.pack(padx=20, pady=10, fill="x")

    tk.Label(form_frame, text="Table Code:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_table = tk.Entry(form_frame, width=12)
    entry_table.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Name:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
    entry_name = tk.Entry(form_frame, width=15)
    entry_name.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(form_frame, text="Guests:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_guests = tk.Entry(form_frame, width=12)
    entry_guests.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Hours (1-4):").grid(row=1, column=2, sticky="e", padx=5, pady=5)
    entry_hours = tk.Entry(form_frame, width=15)
    entry_hours.grid(row=1, column=3, padx=5, pady=5)

    book_btn = tk.Button(
        form_frame, 
        text="Book Table", 
        bg="#4CAF50", 
        fg="white", 
        font=("Helvetica", 9, "bold"),
        command=lambda: book_table_action(entry_table, entry_name, entry_guests, entry_hours, table_widget)
    )
    book_btn.grid(row=0, column=4, rowspan=2, padx=15, pady=5, sticky="nesw")

    # --- Cancellation & Stats Frame ---
    action_frame = tk.LabelFrame(root, text=" Management & Search ", font=("Helvetica", 10, "bold"), padx=10, pady=10)
    action_frame.pack(padx=20, pady=10, fill="x")

    tk.Label(action_frame, text="Booking ID to Cancel:").pack(side="left", padx=5)
    entry_cancel_id = tk.Entry(action_frame, width=12)
    entry_cancel_id.pack(side="left", padx=5)

    cancel_btn = tk.Button(
        action_frame, 
        text="Cancel Booking", 
        bg="#f44336", 
        fg="white", 
        command=lambda: cancel_booking_action(entry_cancel_id, table_widget)
    )
    cancel_btn.pack(side="left", padx=10)

    analytics_btn = tk.Button(
        action_frame, 
        text="Search & Summary Stats", 
        bg="#2196F3", 
        fg="white", 
        command=show_analytics
    )
    analytics_btn.pack(side="right", padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()