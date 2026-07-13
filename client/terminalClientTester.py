import sqlite3
import os

# Folder where python_file.py lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the database
db_path = os.path.join(script_dir, "..", "database", "sqlite-python", "my.db")

# Convert to absolute path
db_path = os.path.abspath(db_path)


def runSQL(statement):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(statement)
            conn.commit()
            print("SQL statements executed successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to execute SQL statements:", e)

def addMessage(senderID, chatRoomID, content):
    runSQL(f"""
        INSERT INTO Messages (senderID, chatRoomID, content) VALUES ({senderID}, {chatRoomID}, "{content}");
    """)

def addAccount(username, password):
    runSQL(f"""
        INSERT INTO Accounts (username, password) VALUES ("{username}", "{password}");
    """)

def addChatRoom(name, user1ID, user2ID):
    runSQL(f"""
        INSERT INTO ChatRooms (name, user1ID, user2ID) VALUES ("{name}", {user1ID}, {user2ID});
    """)

# Main UI
print("\n -- RENICHAT DATABASE ACCESSER - BUILD 0.1.1 -- \n")

run = True
while run:
    print("1. Add message")
    print("0. Exit")
    print("-1. Custom Query")
    choice = input("Enter your choice: ")
    if choice == "1":
        senderID = int(input("Enter sender ID: "))
        chatRoomID = int(input("Enter chat room ID: "))
        content = input("Enter message content: ")
        addMessage(senderID, chatRoomID, content)
    elif choice == "0":
        run = False
        print("Quitting!")
    elif choice == "-1":
        print("Enter a valid SQL statement:")
        custom_command = input("> ")
        runSQL(custom_command)
    else:
        print("(!) Invalid choice")
    print()