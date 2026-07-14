import sqlite3

sql_statements = [ 
    """CREATE TABLE IF NOT EXISTS Accounts (
            accountID INTEGER PRIMARY KEY, 
            username text NOT NULL, 
            password text NOT NULL,
            salt text NOT NULL
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
        );""",
]

# Create an account:
#   INSERT INTO Accounts (Username, Password) VALUES ('text', 'text');

# create a database connection
try:
    with sqlite3.connect('my.db') as conn:
        # create a cursor
        cursor = conn.cursor()

        # execute statements
        for statement in sql_statements:
            cursor.execute(statement)

        # commit the changes
        conn.commit()

        print("Tables created successfully.")
except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)
