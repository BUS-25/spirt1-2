import json
from datetime import datetime
import os

# File to store daily health records
DATA_FILE = "daily_health_records.json"

# Predefined simple health options for older adults
HEALTH_OPTIONS = [
    "Good",
    "Okay",
    "Tired",
    "Pain",
    "Unwell"
]

def load_records():
    """Load existing health records from file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_records(records):
    """Save updated health records to file."""
    with open(DATA_FILE, "w") as file:
        json.dump(records, file, indent=4)

def display_menu():
    """Display health options to the user."""
    print("\n=== Daily Health Input ===")
    print("Please select your health status for today:")
    for i, option in enumerate(HEALTH_OPTIONS, start=1):
        print(f"{i}. {option}")

def get_user_choice():
    """Get user's selected health option."""
    while True:
        try:
            choice = int(input("\nEnter your choice (1-5): "))
            if 1 <= choice <= len(HEALTH_OPTIONS):
                return HEALTH_OPTIONS[choice - 1]
            else:
                print("Invalid option. Please select a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def record_health_status():
    """Main feature: record user's daily health status."""
    display_menu()
    selected_status = get_user_choice()

    # Load previous data
    records = load_records()

    # Create new entry
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": selected_status
    }

    # Save record
    records.append(entry)
    save_records(records)

    # Output confirmation
    print("\n✔ Your health status has been recorded successfully!")
    print(f"Date: {entry['date']}")
    print(f"Selected Status: {entry['status']}\n")

if __name__ == "__main__":
    record_health_status()
