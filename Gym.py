import sqlite3
from datetime import date

# ---------------- DATABASE ----------------

conn = sqlite3.connect("gym.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    phone TEXT,
    gender TEXT,
    plan TEXT,
    join_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS trainers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    specialization TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    amount REAL,
    payment_date TEXT,
    FOREIGN KEY(member_id) REFERENCES members(id)
)
""")

conn.commit()


# ---------------- MEMBER FUNCTIONS ----------------

def add_member():
    print("\n--- Add New Member ---")

    name = input("Enter name: ")
    age = int(input("Enter age: "))
    phone = input("Enter phone: ")
    gender = input("Enter gender: ")
    plan = input("Enter plan (Monthly/Quarterly/Yearly): ")

    join_date = str(date.today())

    cursor.execute("""
    INSERT INTO members
    (name, age, phone, gender, plan, join_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, age, phone, gender, plan, join_date))

    conn.commit()

    print("✅ Member added successfully!")


def view_members():
    print("\n--- All Members ---")

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    if not members:
        print("No members found.")
        return

    for member in members:
        print("--------------------------------")
        print("ID       :", member[0])
        print("Name     :", member[1])
        print("Age      :", member[2])
        print("Phone    :", member[3])
        print("Gender   :", member[4])
        print("Plan     :", member[5])
        print("Join Date:", member[6])


def search_member():
    print("\n--- Search Member ---")

    name = input("Enter member name: ")

    cursor.execute(
        "SELECT * FROM members WHERE name LIKE ?",
        ('%' + name + '%',)
    )

    members = cursor.fetchall()

    if not members:
        print("❌ Member not found.")
        return

    for member in members:
        print("--------------------------------")
        print("ID       :", member[0])
        print("Name     :", member[1])
        print("Age      :", member[2])
        print("Phone    :", member[3])
        print("Gender   :", member[4])
        print("Plan     :", member[5])
        print("Join Date:", member[6])


def update_member():
    print("\n--- Update Member ---")

    member_id = int(input("Enter member ID: "))

    cursor.execute(
        "SELECT * FROM members WHERE id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    if not member:
        print("❌ Member not found.")
        return

    name = input("Enter new name: ")
    age = int(input("Enter new age: "))
    phone = input("Enter new phone: ")
    gender = input("Enter new gender: ")
    plan = input("Enter new plan: ")

    cursor.execute("""
    UPDATE members
    SET name=?, age=?, phone=?, gender=?, plan=?
    WHERE id=?
    """, (name, age, phone, gender, plan, member_id))

    conn.commit()

    print("✅ Member updated successfully!")


def delete_member():
    print("\n--- Delete Member ---")

    member_id = int(input("Enter member ID: "))

    cursor.execute(
        "SELECT * FROM members WHERE id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    if not member:
        print("❌ Member not found.")
        return

    cursor.execute(
        "DELETE FROM members WHERE id = ?",
        (member_id,)
    )

    conn.commit()

    print("✅ Member deleted successfully!")


# ---------------- TRAINER FUNCTIONS ----------------

def add_trainer():
    print("\n--- Add Trainer ---")

    name = input("Enter trainer name: ")
    phone = input("Enter phone: ")
    specialization = input("Enter specialization: ")

    cursor.execute("""
    INSERT INTO trainers
    (name, phone, specialization)
    VALUES (?, ?, ?)
    """, (name, phone, specialization))

    conn.commit()

    print("✅ Trainer added successfully!")


def view_trainers():
    print("\n--- All Trainers ---")

    cursor.execute("SELECT * FROM trainers")
    trainers = cursor.fetchall()

    if not trainers:
        print("No trainers found.")
        return

    for trainer in trainers:
        print("--------------------------------")
        print("ID            :", trainer[0])
        print("Name          :", trainer[1])
        print("Phone         :", trainer[2])
        print("Specialization:", trainer[3])


# ---------------- PAYMENT FUNCTIONS ----------------

def add_payment():
    print("\n--- Add Payment ---")

    member_id = int(input("Enter member ID: "))

    cursor.execute(
        "SELECT name FROM members WHERE id=?",
        (member_id,)
    )

    member = cursor.fetchone()

    if not member:
        print("❌ Member not found.")
        return

    amount = float(input("Enter payment amount: "))
    payment_date = str(date.today())

    cursor.execute("""
    INSERT INTO payments
    (member_id, amount, payment_date)
    VALUES (?, ?, ?)
    """, (member_id, amount, payment_date))

    conn.commit()

    print("✅ Payment added successfully!")


def view_payments():
    print("\n--- Payment History ---")

    cursor.execute("""
    SELECT payments.id,
           members.name,
           payments.amount,
           payments.payment_date
    FROM payments
    JOIN members
    ON payments.member_id = members.id
    """)

    payments = cursor.fetchall()

    if not payments:
        print("No payment records found.")
        return

    for payment in payments:
        print("--------------------------------")
        print("Payment ID:", payment[0])
        print("Member    :", payment[1])
        print("Amount    : ₹", payment[2])
        print("Date      :", payment[3])


# ---------------- DASHBOARD ----------------

def dashboard():
    print("\n========== GYM DASHBOARD ==========")

    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM trainers")
    total_trainers = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM payments")
    total_payment = cursor.fetchone()[0]

    print("Total Members  :", total_members)
    print("Total Trainers :", total_trainers)
    print("Total Revenue  : ₹", total_payment)

    print("===================================")


# ---------------- MAIN MENU ----------------

def main():

    while True:

        print("\n")
        print("======================================")
        print("       🏋️ GYM MANAGEMENT SYSTEM")
        print("======================================")
        print("1. Add Member")
        print("2. View Members")
        print("3. Search Member")
        print("4. Update Member")
        print("5. Delete Member")
        print("6. Add Trainer")
        print("7. View Trainers")
        print("8. Add Payment")
        print("9. View Payments")
        print("10. Dashboard")
        print("0. Exit")
        print("======================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_member()

        elif choice == "2":
            view_members()

        elif choice == "3":
            search_member()

        elif choice == "4":
            update_member()

        elif choice == "5":
            delete_member()

        elif choice == "6":
            add_trainer()

        elif choice == "7":
            view_trainers()

        elif choice == "8":
            add_payment()

        elif choice == "9":
            view_payments()

        elif choice == "10":
            dashboard()

        elif choice == "0":
            print("Thank you for using Gym Management System!")
            conn.close()
            break

        else:
            print("❌ Invalid choice. Try again.")


# Start program
main()