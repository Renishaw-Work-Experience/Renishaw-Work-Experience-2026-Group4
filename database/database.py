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
    messages = [{"messageID": row[0], "senderID": row[1], "chatRoomID": row[2], "content": row[3], "timeSent": row[4]} for row in rows]
    return messages

def printChatRoom(roomID):
    messages = getMessages(roomID)
    for message in messages:
        print(f"\n{getUsernameByID(message["senderID"])} - {message["timeSent"]}")
        print(f"  {message["content"]}")
    

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
