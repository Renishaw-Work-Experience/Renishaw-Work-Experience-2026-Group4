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

        hash_value = SQLF.getPasswordHashFromUsername(username)
        if hash_value is None:
            print("Username not found.")
            return False

        if isinstance(hash_value, str):
            if hash_value.startswith("b'") or hash_value.startswith('b"'):
                import ast
                try:
                    hash_value = ast.literal_eval(hash_value)
                except (ValueError, SyntaxError):
                    hash_value = hash_value.encode('utf-8')
            else:
                hash_value = hash_value.encode('utf-8')

        try:
            userBytes = userPassword.encode('utf-8')
            result = bcrypt.checkpw(userBytes, hash_value)
        except Exception as exc:
            print("Error checking password:", exc)
            return False

        if result:
            return SQLF.addSession(SQLF.getAccountIDFromUsername(username))
        print("Incorrect password.")
        return False
        return False
