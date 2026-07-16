import sqlite3
import os
import time

# Folder where python_file.py lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the database relative to this module
# This ensures the DB is opened correctly regardless of current working directory.
db_path = os.path.join(script_dir, "sqlite-python", "my.db")

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
        INSERT INTO Messages (senderID, chatRoomID, content,TimeSent) VALUES ({senderID}, {chatRoomID}, "{content}",{time.time()});
    """)

def addAccount(username, password, salt):
    runSQL(f"""
        INSERT INTO Accounts (username, password, salt) VALUES ("{username}", "{password}", "{salt}");
    """)

def addChatRoom(roomID, name, members):
    runSQL(f"""
           INSERT INTO ChatRooms (name, {", ".join([f"userID{members.index(x) + 1}" for x in members])}) VALUES ({name}, {str(members)[1:-1]});
    """)

def addSession(userID, sessionID=None, timestamp=None):
    if sessionID is None:
        sessionID = ""
    if timestamp is None:
        timestamp = ""
    runSQL(f"""
        INSERT INTO Sessions (sessionID, userID, timestamp) VALUES ("{sessionID}", {userID}, "{timestamp}");
    """)

def getUsernameByID(userID):
    return getData("Accounts", "username", "accountID", userID)
    
def getIDByUsername(username):
    return getData("Accounts","accountID","user", username)

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

def getData(table, outputField, queryField, data): # returns data from another field using known data from a specified field
    try:
        rows = getDataByQuery(f"SELECT {outputField} FROM {table} WHERE {queryField} = '{data}';")
        if rows:
            return rows[0][0]
        else:
            return None
    except sqlite3.OperationalError as e:
        print("Failed to retrieve data:", e)
        return None
    
    
def getMessages(roomID, userID = None):
    rows = getDataByQuery(f"SELECT * FROM Messages WHERE chatRoomID = {roomID}{"" if userID == None else f"AND senderID = {userID}"} ORDER BY TimeSent ASC;")
    messages = [{"messageID": row[0], "senderID": row[1], "chatRoomID": row[2], "content": row[3], "timeSent": row[4]} for row in rows]
    return messages

def getRoomsFromUserID(userID):
    # Query all chat rooms where the userID matches any of the 5 member slots
    query = f"""
        SELECT * FROM ChatRooms 
        WHERE userID1 = {userID} 
           OR userID2 = {userID} 
           OR userID3 = {userID} 
           OR userID4 = {userID} 
           OR userID5 = {userID};
    """

    rows = getDataByQuery(query)
    if rows:
        rows = [i[0] for i in rows]
    
    # Return the list of matched rooms (or an empty list if none are found)
    return rows if rows else []


'''
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

def addChatRoom(roomID, name, members):
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
'''
def get_chatroom_users(db_path, roomID):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT userID1, userID2, userID3, userID4, userID5
            FROM ChatRooms
            WHERE roomID = ?
        """, (roomID,))

        room = cursor.fetchone()
        
        user_ids = [userid for userid in room if userid is not None]

        if not user_ids:
            return []

        placeholders = ",".join("?" * len(user_ids))

        cursor.execute(f"""
            SELECT username
            FROM Accounts
            WHERE accountID IN ({placeholders})
        """, user_ids)

        return cursor.fetchall()

def getSessionID(userID):
    return getData("Sessions", "sessionID", "userID", userID)

def getUserIDFromSessionID(SessionID):
    return getData("sessions","userID","sessionID",SessionID)


def addSession(userID, sessionID, timestamp=None):
    if timestamp is None:
        timestamp = time.time()
    runSQL(f"""
        INSERT INTO Sessions (sessionID, userID) VALUES ("{sessionID}", {userID});
    """)

def getChatRoomInfo(RoomID):
    pass