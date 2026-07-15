from flask import Flask, request, jsonify
import time
import sys
from pathlib import Path
import secrets

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from database import database

app = Flask(__name__)

sessionIDs = {}

def verifyUser(sessionID, userID):
    return True
    if sessionID is None or userID is None:
        return False
    try:
        if sessionIDs[sessionID] == userID:
            return True
    except KeyError:
        return False
    return False


def requireAuthenticatedUser():
    data = request.get_json(silent=True) or {}
    if not data and request.args:
        data = request.args.to_dict()

    session_id = (
        data.get("sessionID")
        or data.get("session_id")
        or request.headers.get("sessionID")
        or request.headers.get("SessionID")
    )
    userID = (
        data.get("userID")
        or data.get("userID")
        or request.headers.get("userID")
        or request.headers.get("UserID")
    )

    if not verifyUser(session_id, userID):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    return None

def requirePermission(userID, roomID, accessType="w"):
    pass


@app.route('/listener', methods=['POST'])
def sendMessage():
    auth_error = requireAuthenticatedUser()
    if auth_error:
        return auth_error

    data = request.get_json()
    data_dict = data.to_dict()
    database.addMessage(data_dict["senderID"],data_dict["roomID"],data_dict["message"])
    # Process incoming data
    return jsonify({"status": "received", "data": data}), 200

    return jsonify({"status": "listening"}), 200

@app.route('/listener/chat_history', methods=['GET'])
def requestChatHistory():
    auth_error = requireAuthenticatedUser()
    if auth_error:
        return auth_error

    data = request.args
    data_dict = data.to_dict()
    roomID = data_dict["roomID"]
    messages = database.getMessages(roomID)

    return jsonify({"status": "chat history requested", "roomID": roomID,
                     "messages": [{"timestamp": time.time(), "message": message["content"],"senderID": message["senderID"]} for message in messages]}), 200

@app.route('/listener/chat_create', methods=['POST'])
def createChatRoomRequest():
    auth_error = requireAuthenticatedUser()
    if auth_error:
        return auth_error

    data = request.get_json()
    data_dict = data.to_dict()
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
    auth_error = requireAuthenticatedUser()
    if auth_error:
        return auth_error

    data = request.get_json()
    data_dict = data.to_dict()
    try:
        roomID = data["roomID"]
        userID = data["userID"]
        response = call_database("add_member", roomID, userID)
        if response is None:
            return jsonify({"status": "error", "message": "Failed to invite user to chat room"}), 500

    except KeyError:
        return jsonify({"status": "error", "message": "Missing data in request data"}), 400
    return jsonify({"status": "user invited", "data": data}), 200

@app.route('/listener/get_user_id', methods=['POST'])
def getUserId():
    auth_error = requireAuthenticatedUser()
    if auth_error:
        return auth_error

    data = request.get_json()
    data_dict = data.to_dict()
    try:
        username = data["username"]
        
        userID = "user_" + username
        return jsonify({"status": "user found", "userID": userID}), 200

    except KeyError:
        return jsonify({"status": "error", "message": "Missing username in request data"}), 400

@app.route('/listener/chat_info', methods=['GET'])
def getChatRoomInfo():
    auth_error = requireAuthenticatedUser()
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
    data = request.args 
    password = data.get("password")
    username = data.get("username")
    #actually verify login later
    if True:
        sessionID =  secrets.token_hex(16)
        userID = ""
        return jsonify({"status": "login successful","sessionID":sessionID,"userID":userID})
    else:
        return jsonify({"status"})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)   


