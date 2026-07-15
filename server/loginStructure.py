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
            bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes, salt)
            SQLF.addAccount(username, hash)
            print("Account created successfully.")
        except:
             print("Error creating account")
    
def login(username, userPassword):
        hash = SQLF.getPasswordHashFromUsername()
        userBytes = userPassword.encode('utf-8')
        result = bcrypt.checkpw(userBytes, hash)
        if result:
              SQLF.addSession(SQLF.getAccountIDFromUsername(username))
        else:
            print("Incorrect password.")