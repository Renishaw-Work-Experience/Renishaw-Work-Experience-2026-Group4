import sqlite3
import os

# Folder where python_file.py lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the database
# db_path = os.path.join("database", "sqlite-python", "my.db")
db_path = "my.db"

# Convert to absolute path
db_path = os.path.abspath(db_path)

try:
    with sqlite3.connect(db_path) as conn:
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")

except sqlite3.OperationalError as e:
    print("Failed to open database:", e)

sql_statements = [
    """CREATE TABLE IF NOT EXISTS Accounts (
            accountID INTEGER PRIMARY KEY, 
            username TEXT NOT NULL, 
            password TEXT NOT NULL,
            salt TEXT NOT NULL
        );
        """,
    """
        CREATE TABLE IF NOT EXISTS Messages (
            messageID INTEGER PRIMARY KEY,
            senderID INTEGER NOT NULL,
            chatRoomID INTEGER NOT NULL,
            content TEXT NOT NULL,
            TimeSent DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY (senderID) REFERENCES Accounts(accountID),
            FOREIGN KEY (chatRoomID) REFERENCES ChatRooms(roomID)
        );
        """,
    """
        CREATE TABLE IF NOT EXISTS Sessions (
            sessionID TEXT PRIMARY KEY DEFAULT (hex(randomblob(16))),
            userID INTEGER NOT NULL,
            FOREIGN KEY (userID) REFERENCES Accounts(accountID)
        );
        """,
    """
        CREATE TABLE IF NOT EXISTS ChatRooms (
            roomID INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            user1ID INTEGER,
            user2ID INTEGER,
            user3ID INTEGER,
            user4ID INTEGER,
            user5ID INTEGER,
            FOREIGN KEY (user1ID) REFERENCES Accounts(accountID),
            FOREIGN KEY (user2ID) REFERENCES Accounts(accountID),
            FOREIGN KEY (user3ID) REFERENCES Accounts(accountID),
            FOREIGN KEY (user4ID) REFERENCES Accounts(accountID),
            FOREIGN KEY (user5ID) REFERENCES Accounts(accountID)
        );
        """
]

# Create an account:
#   INSERT INTO Accounts (Username, Password) VALUES ('text', 'text');

# create a database connection
try:
    with sqlite3.connect(db_path) as conn:
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
