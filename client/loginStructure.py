import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import SQLite_Functions as SQLF
import sqlite3

accountIDLogged = None
chatRoomIDLogged = None

run = True

while run:
    print("1. Create Account")
    print("2. Log in")
    print("\n0. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        SQLF.addAccount(username, password)
        print("Account created successfully.")
        accountIDLogged = SQLF.getData("Accounts", "accountID", "username",  f"{username}")
    if choice == "2":
        username = input("Enter username: ")
        if SQLF.getData("Accounts", "accountID", "username", f"{username}") != None:
            password = input("Enter password: ")
            if SQLF.getData("Accounts", "password", "accountID", f"{SQLF.getData('Accounts', 'accountID', 'username', f'{username}')}") == password:
                print("Login successful.")
                accountIDLogged = SQLF.getData("Accounts", "accountID", "username",  f"{username}")
            else:
                print("Incorrect password.")
        else:
            print("Username not found.")
    if choice == "0":
        run = False
    while accountIDLogged != None:
        print("Main Functions will go here")
        print("Press enter to sign out")
        input()
        accountIDLogged = None