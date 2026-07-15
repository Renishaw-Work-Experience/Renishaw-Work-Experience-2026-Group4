import os
import database
import database

# Folder where python_file.py lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the database
db_path = os.path.join(script_dir, "..", "database", "sqlite-python", "my.db")

# Convert to absolute path
db_path = os.path.abspath(db_path)


# Main UI
print("\n -- RENICHAT DATABASE ACCESSER - BUILD 1.0.1 -- \n")

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
        database.addMessage(senderID, chatRoomID, content)
        database.addMessage(senderID, chatRoomID, content)
    elif choice == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        database.addAccount(username, password)
        database.addAccount(username, password)
    elif choice == "3":
        name = input("Enter chat room name: ")
        user1ID = int(input("Enter user 1 ID: "))
        user2ID = int(input("Enter user 2 ID: "))
        database.addChatRoom(name, user1ID, user2ID)
        database.addChatRoom(name, user1ID, user2ID)
    elif choice == "4":
        roomID = int(input("Enter chat room ID: "))
        database.printChatRoom(roomID)
        database.printChatRoom(roomID)

    elif choice == "0":
        run = False
        print("Quitting!")
    elif choice == "-1":
        print("Enter a valid SQL statement:")
        custom_command = input("> ")
        database.runSQL(custom_command)
        database.runSQL(custom_command)
    elif choice == "-2":
        print("Enter a valid SQL SELECT query:")
        custom_command = input("> ")
        rows = database.getDataByQuery(custom_command)
        rows = database.getDataByQuery(custom_command)
        for row in rows:
            print(row)
    else:
        print("(!) Invalid choice")
    print()