#!/usr/bin/env python3
# Library Study Table Booking System
import os
from datetime import datetime


tables = [
    {"id": 1, "Name": "Table 1"},
    {"id": 2, "Name": "Table 2"},
    {"id": 3, "Name": "Table 3"},
    {"id": 4, "Name": "Table 4"},
    {"id": 5, "Name": "Table 5"}
]

bookings = []

time_slots = [
    "09:00-12:00",
    "13:00-16:00",
    "16:00-19:00"
]

def is_available(table_id, time_slot, bookings):
    for booking in bookings:
        if (booking["table_id"] == table_id
                and booking["time_slot"] == time_slot):
            return False
    return True


def show_tables(tables, bookings):
    print("\n--- TABLE STATUS ---")

    for table in tables:
        print(f"\nTable {table['id']}:")

        for slot in time_slots:
            GREEN = "\033[92m"
            RED = "\033[91m"
            RESET = "\033[0m"


            if is_available(table["id"], slot, bookings):
                status = f"{GREEN}Available{RESET}"
            else:
                status = f"{RED}Booked{RESET}"

            print(f"  {slot} : {status}")


def book_table(tables, bookings):
    print("\n--- BOOK A TABLE ---")

    student_id = input("Enter student ID: ").strip()

    if len(student_id) != 8 or not student_id.isdigit():
        print("\033[91mError: Student ID must be an 8-digit number.\033[0m")
        return

    try:
        table_id = int(input("Enter table number (1-5): "))
    except ValueError:
        print("\033[91mError: Table number must be a number.\033[0m")
        return

    table_exists = False

    for table in tables:
        if table["id"] == table_id:
            table_exists = True
            break

    if not table_exists:
        print("Error: Table does not exist.")
        return

    print("\nAvailable time slots:")
    for i, slot in enumerate(time_slots, start=1):
        print(f"{i}. {slot}")

    try:
        choice = int(input("Choose time slot (1-3): "))
    except ValueError:
        print("Error: Please enter a number.")
        return

    if choice < 1 or choice > len(time_slots):
        print("Error: Invalid time slot.")
        return

    time_slot = time_slots[choice - 1]

    RED = "\033[91m"
    RESET = "\033[0m"

    if not is_available(table_id, time_slot, bookings):
        print(f"{RED}Sorry, this table is already booked.{RESET}")
        return

    booking = {
        "booking_id": len(bookings) + 1,
        "student_id": student_id,
        "table_id": table_id,
        "time_slot": time_slot
    }

    bookings.append(booking)
    save_history("Booking", booking)

    print("\nBooking successful!")

    print(f"Booking ID: {booking['booking_id']}")
    print(f"Student ID: {student_id}")
    print(f"Table: {table_id}")
    print(f"Time: {time_slot}")


def view_bookings(bookings):
    print("\n--- MY BOOKINGS ---")

    student_id = input("Enter student ID: ").strip()

    found = False

    for booking in bookings:
        if booking["student_id"] == student_id:
            print(
                f"Booking ID: {booking['booking_id']} | "
                f"Table: {booking['table_id']} | "
                f"Time: {booking['time_slot']}"
            )
            found = True

    if not found:
        print("No bookings found.")


def cancel_booking(bookings):
    print("\n--- CANCEL BOOKING ---")

    try:
        booking_id = int(input("Enter booking ID: "))
    except ValueError:
        print("Error: Booking ID must be a number.")
        return

    for booking in bookings:
        if booking["booking_id"] == booking_id:
            student_id = input("Enter student ID: ").strip()

            if booking["student_id"] != student_id:
                print("Error: Student ID does not match.")
                return

            bookings.remove(booking)
            save_history("Cancellation", booking)
            print("Booking cancelled successfully!")
            return

    print("Error: Booking ID not found.")


def main():
    while True:
        print("\n==============================")
        print(" LIBRARY TABLE BOOKING SYSTEM")
        print("==============================")   
        print("1. Show table status")
        print("2. Book a table")
        print("3. View my bookings")
        print("4. Cancel a booking")
        print("5. View booking history")
        print("6. Exit")

        choice = input("Select menu (1-6): ").strip()

        if choice == "1":
            show_tables(tables, bookings)
        elif choice == "2":
            book_table(tables, bookings)
        elif choice == "3":
            view_bookings(bookings)
        elif choice == "4":
            cancel_booking(bookings)
        elif choice == "5":
            view_history()
        elif choice == "6":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid menu. Please select 1-6.")

            print("Thank you for using the system!")
            break


HISTORY_FILE = "booking_history.txt"


def view_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = file.read()

        if history.strip():
            print()
            print("========================================")
            print("             BOOKING HISTORY")
            print("========================================")
            print(history)
        else:
            print("No booking history found.")

    except FileNotFoundError:
        print("No booking history found.")


def save_history(action, booking):
    current_time = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"Date/Time: {current_time}\n"
            f"Action: {action}\n"
            f"Booking ID: {booking['booking_id']}\n"
            f"Student ID: {booking['student_id']}\n"
            f"Table: {booking['table_id']}\n"
            f"Time Slot: {booking['time_slot']}\n"
            "------------------------------\n"
        )


def view_history():
    print("\n--------- BOOKING HISTORY ---------")

    if not os.path.exists(HISTORY_FILE):
        print("No booking history found.")
        return

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        history = file.read()

    if history.strip():
        print(history)
    else:
        print("No booking history found.")

main()
