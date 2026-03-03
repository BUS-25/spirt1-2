import json
from datetime import datetime
import os

# File to store daily health records
DATA_FILE = "daily_health_records.json"

# Simple health status options
HEALTH_OPTIONS = [
    "Good",
    "Okay",
    "Tired",
    "Pain",
    "Unwell"
]

def load_records():
    """Load health records from a JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_records(records):
    """Save updated health records into JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(records, file, indent=4)

def display_menu():
    """Display basic health options."""
    print("\n=== Daily Health Input ===")
    print("Please select your health status:")
    for i, option in enumerate(HEALTH_OPTIONS, start=1):
        print(f"{i}. {option}")

def get_user_choice():
    """Choose health status."""
    while True:
        try:
            choice = int(input("\nEnter your choice (1-5): "))
            if 1 <= choice <= len(HEALTH_OPTIONS):
                return HEALTH_OPTIONS[choice - 1]
            print("Invalid option. Enter 1–5.")
        except ValueError:
            print("Invalid input. Enter a number.")

def get_heart_rate():
    """Input heart rate."""
    while True:
        try:
            hr = int(input("Enter heart rate (bpm): "))
            if 30 <= hr <= 200:
                return hr
            print("Heart rate must be between 30–200.")
        except ValueError:
            print("Enter a valid number.")

def get_blood_pressure():
    """Input systolic and diastolic blood pressure."""
    while True:
        try:
            sys = int(input("Enter systolic BP (mmHg): "))
            dia = int(input("Enter diastolic BP (mmHg): "))
            if 70 <= sys <= 250 and 40 <= dia <= 150:
                return f"{sys}/{dia}"
            print("BP must be realistic (Sys: 70–250, Dia: 40–150).")
        except ValueError:
            print("Enter valid numbers.")

def record_health_status():
    """Record full daily health data."""
    display_menu()
    status = get_user_choice()
    hr = get_heart_rate()
    bp = get_blood_pressure()

    records = load_records()

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": status,
        "heart_rate": hr,
        "blood_pressure": bp
    }

    records.append(entry)
    save_records(records)

    print("\n✔ Health data saved!")
    print(f"Date: {entry['date']}")
    print(f"Status: {entry['status']}")
    print(f"Heart Rate: {entry['heart_rate']} bpm")
    print(f"Blood Pressure: {entry['blood_pressure']}\n")

def view_history():
    """Display all recorded health entries."""
    records = load_records()
    if not records:
        print("\nNo records found.\n")
        return

    print("\n=== Health Record History ===\n")
    for i, rec in enumerate(records, start=1):
        print(f"{i}. {rec['date']} - {rec['status']} "
              f"| HR: {rec['heart_rate']} bpm | BP: {rec['blood_pressure']}")
    print()

def delete_record():
    """Delete a selected record."""
    records = load_records()
    if not records:
        print("\nNo records to delete.\n")
        return

    view_history()
    while True:
        try:
            index = int(input("Enter record number to delete (0 to cancel): "))
            if index == 0:
                print("Cancel delete.\n")
                return
            if 1 <= index <= len(records):
                removed = records.pop(index - 1)
                save_records(records)
                print(f"\n✔ Deleted record from {removed['date']} successfully!\n")
                return
            print("Invalid selection.")
        except ValueError:
            print("Enter a valid number.")

def main_menu():
    """Main interactive menu."""
    while True:
        print("\n=== Health Monitoring System ===")
        print("1. Record Today's Health Status")
        print("2. View History")
        print("3. Delete a Record")
        print("4. Exit")

        try:
            choice = int(input("Select an option: "))
            if choice == 1:
                record_health_status()
            elif choice == 2:
                view_history()
            elif choice == 3:
                delete_record()
            elif choice == 4:
                print("Goodbye!")
                break
            else:
                print("Invalid choice, select 1–4.")
        except ValueError:
            print("Enter a valid number.")

if __name__ == "__main__":
    main_menu()
