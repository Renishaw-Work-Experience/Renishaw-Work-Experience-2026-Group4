import sqlite3

sql_statements = [
    # Remove all data from the tables
    """
        DELETE FROM Accounts;
    """,
    """
        DELETE FROM Messages;
    """,
    """
        DELETE FROM ChatRooms;
    """,
    # Insert new test data into the tables
    """
        INSERT INTO Accounts (username, password) VALUES ('username1', 'password1');
    """
        ,
    """
        INSERT INTO Accounts (username, password) VALUES ('username2', 'password2');
    """,
    """
        INSERT INTO Accounts (username, password) VALUES ('username3', 'password3');
    """,
    """
        INSERT INTO ChatRooms (name, user1ID, user2ID) VALUES ('Test chat room', 1, 2);
    """,
    """
        INSERT INTO Messages (senderID, chatRoomID, content) VALUES (1, 1, "Test message");
    """,
]

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

        print("Added data succesfully.")
except sqlite3.OperationalError as e:
    print("Failed to add data:", e)
