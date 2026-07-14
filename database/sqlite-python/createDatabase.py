import sqlite3
import os

# Folder where python_file.py lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the database
db_path = os.path.join("database", "sqlite-python", "my.db")

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
