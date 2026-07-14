import sqlite3

sql_statements = [ 
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
        INSERT INTO Messages (senderID, chatRoomID, content) VALUES (111, 222, "Test message");
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
