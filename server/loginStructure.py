import sys
from pathlib import Path
import bcrypt

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from database import database as SQLF

accountIDLogged = None
chatRoomIDLogged = None

def createAccount(username, password):
        try:
            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt)
            SQLF.addAccount(username, hashed_password.decode('utf-8'), salt.decode('utf-8'))
            print("Account created successfully.")
        except Exception as exc:
            print("Error creating account", exc)
    
def login(username, userPassword):
        if username is None or userPassword is None:
            return False

        hash_value = SQLF.getPasswordHashFromUsername(username).encode('utf-8') if SQLF.getPasswordHashFromUsername(username) is not None else None
        if hash_value is None:
            print("Username not found.")
            return False
        result = False
        try:
            userBytes = userPassword.encode('utf-8')
            result = bcrypt.checkpw(userBytes, hash_value)
            return True if result else False
        except Exception as exc:
            print("Error checking password:", exc)
            return False
        return False
        
