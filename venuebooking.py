from datetime import datetime

# ------------------------------
# In-memory Data Storage
# ------------------------------
users = {}
venues = {
    "V001": {"name": "Conference Hall A", "capacity": 100, "bookings": []},
    "V002": {"name": "Banquet Hall B", "capacity": 250, "bookings": []},
    "V003": {"name": "Outdoor Garden", "capacity": 500, "bookings": []},
}
admins = {"admin": "admin123"}  # simple admin account

# ------------------------------
# Helper Functions
# ------------------------------
def register():
    username = input("Enter username: ")
    if username in users:
        print("⚠️ Username already exists.")
        return
    password = input("Enter password: ")  # replaced getpass
    users[username] = {"password": password, "bookings": []}
    print("✅ Registration successful!")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")  # replaced getpass
    if username in users and users[username]["password"] == password:
        print(f"✅ Welcome back {username}!")
        return username, "user"
    elif username in admins and admins[username] == password:
        print("✅ Admin login successful!")
        return username, "admin"
    else:
        print("❌ Invalid credentials.")
        return None, None

def show_venues():
    print("\n📌 Available Venues:")
    for vid, v in venues.items():
        print(f"{vid} - {v['name']} | Capacity: {v['capacity']} | Bookings: {len(v['bookings'])}")

def book_venue(user):
    show_venues()
    vid = input("Enter Venue ID: ")
    if vid not in venues:
        print("❌ Invalid Venue ID.")
        return
    date_str = input("Enter booking date (YYYY-MM-DD): ")
    time_str = input("Enter booking time (HH:MM): ")
    try:
        booking_datetime = datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("❌ Invalid date/time format.")
        return
    # Check if slot is already booked
    for booking in venues[vid]["bookings"]:
        if booking["datetime"] == booking_datetime:
            print("❌ Slot already booked.")
            return
    # Add booking
    venues[vid]["bookings"].append({"user": user, "datetime": booking_datetime})
    users[user]["bookings"].append({"venue": vid, "datetime": booking_datetime})
    print(f"✅ Booking confirmed for {venues[vid]['name']} at {booking_datetime}")

def cancel_booking(user):
    if not users[user]["bookings"]:
        print("❌ No bookings to cancel.")
        return
    print("\n📅 Your Bookings:")
    for i, b in enumerate(users[user]["bookings"], start=1):
        print(f"{i}. {venues[b['venue']]['name']} on {b['datetime']}")
    choice = int(input("Enter booking number to cancel: "))
    if 1 <= choice <= len(users[user]["bookings"]):
        booking = users[user]["bookings"].pop(choice - 1)
        venues[booking["venue"]]["bookings"] = [
            b for b in venues[booking["venue"]]["bookings"] if not (b["user"] == user and b["datetime"] == booking["datetime"])
        ]
        print("✅ Booking canceled.")
    else:
        print("❌ Invalid choice.")

def view_bookings(user):
    if not users[user]["bookings"]:
        print("📭 No bookings yet.")
        return
    print("\n📅 Your Bookings:")
    for b in users[user]["bookings"]:
        print(f"- {venues[b['venue']]['name']} on {b['datetime']}")

# ------------------------------
# Admin Functions
# ------------------------------
def add_venue():
    vid = input("Enter new Venue ID: ")
    if vid in venues:
        print("❌ Venue ID already exists.")
        return
    name = input("Enter venue name: ")
    capacity = int(input("Enter capacity: "))
    venues[vid] = {"name": name, "capacity": capacity, "bookings": []}
    print("✅ Venue added successfully.")

def remove_venue():
    show_venues()
    vid = input("