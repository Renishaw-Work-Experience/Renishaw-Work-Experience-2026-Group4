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

def addChatRoom(name, members):
    runSQL(f"""
           INSERT INTO ChatRooms (name, {", ".join([f"userID{members.index(x) + 1}" for x in members])}) VALUES ({name}, {str(members)[1:-1]});
    """)

def getUsernameByID(userID):
    rows = getDataByQuery(f"SELECT username FROM Accounts WHERE accountID = {userID};")
    if rows:
        return rows[0][0]
    else:
        return None

def getMessages(roomID, userID = None):
    rows = getDataByQuery(f"SELECT * FROM Messages WHERE chatRoomID = {roomID}{"" if userID == None else f"AND senderID = {userID}"} ORDER BY TimeSent ASC;")
    return rows

def printChatRoom(roomID):
    rows = getMessages(roomID)
    for row in rows:
        print(f"\n{getUsernameByID(row[1])} - {row[4]}")
        print(f"  {row[3]}")

# def getData(table_name, fields : list = "*"): # Test data retrieval
#     if fields == "*":
#         fields_str = "*"
#     else:
#         fields_str = ", ".join(fields)
#     try:
#         with sqlite3.connect(db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute(f"SELECT {fields_str} FROM {table_name};")
#             rows = cursor.fetchall()
#             return rows
#     except sqlite3.OperationalError as e:
#         print("Failed to retrieve data:", e)
#         return None
    
def getDataByQuery(query):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    except sqlite3.OperationalError as e:
        print("Failed to retrieve data:", e)
        return None

# Main UI
def main():
    print("\n -- RENICHAT DATABASE ACCESSER - BUILD 1.0.1 -- \n")

    while True:
        print("1. Add message")
        print("2. Add account")
        print("3. Add chat room")
        print("4. Retrieve chat room")
        print("\n0. Exit")
        print("-1. Custom Query")
        print("-2. Custom Retrieve Query")
        choice = input("Enter your choice: ")
        if choice == "1":
            senderID = int(input("Enter sender ID: "))
            chatRoomID = int(input("Enter chat room ID: "))
            content = input("Enter message content: ")
            addMessage(senderID, chatRoomID, content)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            addAccount(username, password)
        elif choice == "3":
            name = input("Enter chat room name: ")
            user1ID = int(input("Enter user 1 ID: "))
            user2ID = int(input("Enter user 2 ID: "))
            addChatRoom(name, user1ID, user2ID)
        elif choice == "4":
            roomID = int(input("Enter chat room ID: "))
            printChatRoom(roomID)

        elif choice == "0":
            print("Quitting!")
            break
        elif choice == "-1":
            print("Enter a valid SQL statement:")
            custom_command = input("> ")
            runSQL(custom_command)
        else:
            print("(!) Invalid choice")
        print()