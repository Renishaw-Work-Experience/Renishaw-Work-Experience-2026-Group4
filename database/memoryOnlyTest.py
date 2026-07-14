import sqlite3
import os

def setUpDatabase():
    setupQueries = [ 
        """CREATE TABLE IF NOT EXISTS Accounts (
                accountID INTEGER PRIMARY KEY, 
                username text NOT NULL, 
                password text NOT NULL
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS Messages (
                messageID INTEGER PRIMARY KEY,
                senderID INTEGER NOT NULL,
                chatRoomID INTEGER NOT NULL,
                content text NOT NULL,
                TimeSent DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (senderID) REFERENCES Accounts(accountID),
                FOREIGN KEY (chatRoomID) REFERENCES ChatRooms(roomID)
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS ChatRooms (
                roomID INTEGER PRIMARY KEY,
                name text NOT NULL,
                user1ID INTEGER,
                user2ID INTEGER,
                user3ID INTEGER,
                user4ID INTEGER,
                user5ID INTEGER,
                FOREIGN KEY (user1ID) REFERENCES Accounts(AccountID),
                FOREIGN KEY (user2ID) REFERENCES Accounts(AccountID),
                FOREIGN KEY (user3ID) REFERENCES Accounts(AccountID),
                FOREIGN KEY (user4ID) REFERENCES Accounts(AccountID),
                FOREIGN KEY (user5ID) REFERENCES Accounts(AccountID)
            );
        """,
    ]
    for query in setupQueries:
        runSQL(query)


def runSQL(statement):
    try:
        with sqlite3.connect(":memory:") as conn:
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

def getUsernameByID(userID):
    rows = getDataByQuery(f"SELECT username FROM Accounts WHERE accountID = {userID};")
    if rows:
        return rows[0][0]
    else:
        return None

def printChatRoom(roomID):
    rows = getDataByQuery(f"SELECT * FROM Messages WHERE chatRoomID = {roomID} ORDER BY TimeSent ASC;") # Collect all messages in the chat room with a matching ID
    for row in rows:
        print(f"\n{getUsernameByID(row[1])} - {row[4]}") # Collect the username of the sender and the time sent
        print(f"  {row[3]}") # Collect and print the message contents
    
def getDataByQuery(query):
    try:
        with sqlite3.connect(":memory:") as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    except sqlite3.OperationalError as e:
        print("Failed to retrieve data:", e)
        return None
    
def checkData(table, field, data):
    try:
        with sqlite3.connect(":memory:") as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table} WHERE {field} = '{data}';")
            rows = cursor.fetchall()
            return len(rows) > 0
    except sqlite3.OperationalError as e:
        print("Failed to check data:", e)
        return False

# Main UI
print("\n -- RENICHAT MemoryOnlyTest -- \n")

setUpDatabase()

account = None
chatRoom = None
run = True



run = True
while run:
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
        run = False
        print("Quitting!")
    elif choice == "-1":
        print("Enter a valid SQL statement:")
        custom_command = input("> ")
        runSQL(custom_command)
    elif choice == "-2":
        print("Enter a valid SQL SELECT query:")
        custom_command = input("> ")
        rows = getDataByQuery(custom_command)
        for row in rows:
            print(row)
    else:
        print("(!) Invalid choice")
    print()