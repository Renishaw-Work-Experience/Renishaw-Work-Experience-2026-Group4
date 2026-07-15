# Copy this into any folder that will use the functions from this file.

import sqlite3
import os

# Folder where python_file.py lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the database
db_path = os.path.join("database", "sqlite-python", "my.db")

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

def addChatRoom(roomID, name, members):
    runSQL(f"""
           INSERT INTO ChatRooms (name, {", ".join([f"userID{members.index(x) + 1}" for x in members])}) VALUES ({name}, {str(members)[1:-1]});
    """)

def addSession(userID):
    runSQL(f"""
        INSERT INTO Sessions (userID) VALUES ({userID});
    """)

def getUsernameByID(userID):
    return getData("Accounts", "username", "accountID", userID)
    
def getAccountIDFromUsername(username):
    return getData("Accounts", "accountID", "username", username)

def getPasswordHashFromUsername(username):
    return getData("Accounts", "password", "username", username)

def printChatRoom(roomID):
    rows = getDataByQuery(f"SELECT * FROM Messages WHERE chatRoomID = {roomID} ORDER BY TimeSent ASC;")
    for row in rows:
        print(f"\n{getUsernameByID(row[1])} - {row[4]}")
        print(f"  {row[3]}")
    
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
    
def addUserToChatRoom(chatRoomID, userID):
    runSQL(f"""
        UPDATE ChatRooms SET userID{getNextAvailableUserSlot(chatRoomID)} = {userID} WHERE chatRoomID = {chatRoomID};
    """)

def getNextAvailableUserSlot(chatRoomID):
    rows = getDataByQuery(f"SELECT * FROM ChatRooms WHERE chatRoomID = {chatRoomID};")
    if rows:
        chatRoom = rows[0]
        for i in range(1, 6):  # Assuming a maximum of 5 users per chat room
            if chatRoom[i] is None:
                return i
    return None

def getData(table, field1, field2, data): # returns data from another field using known data from a specified field
    try:
        rows = getDataByQuery(f"SELECT {field1} FROM {table} WHERE {field2} = '{data}';")
        if rows:
            return rows[0][0]
        else:
            return None
    except sqlite3.OperationalError as e:
        print("Failed to retrieve data:", e)
        return None