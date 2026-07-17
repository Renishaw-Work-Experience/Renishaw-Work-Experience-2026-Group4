from flask import Flask, request, jsonify
import time
import sys
from pathlib import Path
import secrets

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from database import database
import SQLite_Functions as SQLF
import loginStructure

app = Flask(__name__)

def verifyUser(sessionID, userID):
    if sessionID is None or userID is None:
        return False
    try:
        if database.getUserIDFromSessionID(sessionID) == userID:
            return True
    except KeyError:
        return False
    return False


def requireAuthenticatedUser(data):
    return None
    if not data and request.args:
        data = request.args.to_dict()

    sessionID = data.get("sessionID")
    userID = data.get("senderID")

    
    if not verifyUser(sessionID, userID):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    return None

def requirePermission(userID, roomID, accessType="w"):
    return True


@app.route('/listener', methods=['POST'])
def sendMessage():
    data = request.get_json()
    auth_error = requireAuthenticatedUser(data) 
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or request.form.to_dict() or request.args.to_dict()
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Invalid data format"}), 400

    sender_id = data.get("senderID") or data.get("sender_id")
    room_id = data.get("roomID") or data.get("room_id")
    message = data.get("message")
    print(f"Received message from senderID: {sender_id}, roomID: {room_id}, message: {message}")
    # if sender_id is None or room_id is None or message is None:
    #     return jsonify({"status": "error", "message": "Missing senderID, roomID, or message"}), 400

    database.addMessage(sender_id, room_id, message)
    print(f"Message stored in database: {message} from senderID: {sender_id} in roomID: {room_id}")
    return jsonify({"status": "received", "timestamp": data.get("timestamp", time.time())}), 200


@app.route('/listener/chat_history', methods=['GET'])
def requestChatHistory():
    auth_error = requireAuthenticatedUser(request.get_json())
    if auth_error:
        return auth_error

    try:
        data = request.get_json()
        data_dict = data
        roomID = data_dict["roomID"]
        messages = database.getMessages(roomID)
    except Exception:
        print(Exception)
        return jsonify({"message ":"internal server error"}), 500

    return jsonify({"status": "chat history requested", "roomID": roomID, "messages": [{"timeSent": message["timeSent"], "content": message["content"],"senderID": message["senderID"]} for message in messages]}), 200

@app.route('/listener/get_all_messages', methods=['GET'])
def getAllMessages():
    print("Received request to retrieve all messages")
    # auth_error = requireAuthenticatedUser(request.get_json())
    print("Authentication check completed")
    # if auth_error:
        # print("Unauthorized access attempt to get all messages")
        # return auth_error
    
    print("Retrieving all messages from the database")
    messages = database.getAllMessages()
    return jsonify({"status": "all messages retrieved", "messages": messages}), 200



@app.route('/listener/chat_create', methods=['POST'])
def createChatRoomRequest():
    auth_error = requireAuthenticatedUser(request.get_json())
    if auth_error:
        return auth_error

    data = request.get_json()
    data_dict = data
    try:
        name = data_dict["name"]
        members = data_dict["members"] + [data_dict["sender"]]
        group_id = name + "_" + data_dict["sender"] + "_" + str(int(time.time()))
        response = database.create_chat_room(name, members)
        if response is None:
            return jsonify({"status": "error", "message": "Failed to create chat room"}), 500

    except KeyError:
        return jsonify({"status": "error", "message": "Missing data in request data"}), 400
    return jsonify({"status": "chat created", "data": data}), 200

@app.route('/listener/chat_invite', methods=['POST'])
def inviteToChat():
    auth_error = requireAuthenticatedUser(request.get_json())
    if auth_error:
        return auth_error

    data = request.get_json()
    data_dict = data.to_dict()
    try:
        roomID = data["roomID"]
        userID = data["userID"]
        database.addUserToChatRoom(roomID, userID)
       
    except KeyError:
        return jsonify({"status": "error", "message": "Missing data in request data"}), 400
    return jsonify({"status": "user invited", "data": data}), 200

@app.route('/listener/get_user_id', methods=['POST'])
def getUserId():
    auth_error = requireAuthenticatedUser(request.get_json())
    if auth_error:
        return auth_error

    data = request.get_json()
    data_dict = data
    try:
        username = data["username"]
        
        userID = data.getIDByUsername(username)
        return jsonify({"status": "user found", "userID": userID}), 200

    except KeyError:
        return jsonify({"status": "error", "message": "Missing username in request data"}), 400

@app.route('/listener/chat_info', methods=['GET'])
def getChatRoomInfo():
    auth_error = requireAuthenticatedUser(request.get_json())
    if auth_error:
        return auth_error

    data = request.args
    data_dict = data.to_dict()
    try:
        roomID = data_dict["roomID"]
        
        chat_info = {
            "roomID": roomID,
            "name": "Sample Chat Room",
            "members": ["user1", "user2", "user3"],
            "created_at": time.time()
        }
        return jsonify({"status": "chat info retrieved", "chat_info": chat_info}), 200

    except KeyError:
        return jsonify({"status": "error", "message": "Missing RoomID in request data"}), 400

@app.route('/listener/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or request.form.to_dict() or request.args.to_dict()
    username = data.get("username")
    password = data.get("password")

    print(f"Login attempt for username: {username}, password: {password}")

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing username or password"}), 400
    sessionID = None
    try:
        if loginStructure.login(username, password):
            sessionID = secrets.token_hex(16)
    except Exception as exc:
        print("Error validating user", exc)
        sessionID = None

    if sessionID:
        userID = SQLF.getAccountIDFromUsername(username)
        database.addSession(userID, sessionID)
        return jsonify({"status": "login successful", "sessionID": sessionID, "userID": userID}), 200

    return jsonify({"status": "error", "message": "Invalid username or password"}), 401

@app.route('/listener/signup', methods=['POST'])
def signup():
    data = request.get_json(silent=True) or request.form.to_dict() or request.args.to_dict()
    password = data.get("password")
    username = data.get("username")

    if not username or not password:
        print("Missing username or password in signup request", data)
        return jsonify({"status": "error", "message": "Missing username or password"}), 400

    try:
        loginStructure.createAccount(username, password)
    except Exception as exc:
        print("Error creating account", exc)
        return jsonify({"status": "error", "message": "Failed to create account"}), 400

    return jsonify({"status": "success", "message": "Account created successfully"}), 201

@app.route('/listener/roomMembership', methods=['POST'])
def room_membership():
    # 1. Force Flask to parse the JSON, even if headers are slightly off

    data = request.get_json(silent=True) 
    
    # 2. Safety check
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
        
    
    sender_id = data.get("senderID")
    if not sender_id:
        return jsonify({"error": "Missing 'senderID' in JSON payload"}), 400
        
    try:
        # 4. Fetch from database and return
        rooms = database.getRoomsFromUserID(sender_id)
        return jsonify({"rooms": rooms}), 200
    except Exception as e:
        # Log database errors so you can see them on the server console
        print(f"Database error: {e}")
        return jsonify({"error": "Internal database error"}), 500


@app.route("/listener/get_username",methods=['GET'])
def getUsernameFromID():
    data = request.args
    auth_error = requireAuthenticatedUser()
    if auth_error:
        return auth_error
    return jsonify(database.getUsernameByID(data["userID"]))


def userDataToJSON(userData):
    user_list = []
    for user in userData:
        user_list.append({
            "accountID": user[0],
            "username": user[1]
        })
    return user_list

@app.route("/listener/get_all_users",methods=['GET'])
def getAllUsers():
    users = database.getDataByQuery("SELECT accountID, username FROM Accounts")
    return jsonify(userDataToJSON(users)), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)   

