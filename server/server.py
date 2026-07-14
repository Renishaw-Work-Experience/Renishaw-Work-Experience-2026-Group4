import os
import sys
import time

from flask import Flask, request, jsonify
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from database import database

app = Flask(__name__)

def verifyUser(sessionID, userID):
    if sessionID is None or userID is None:
        return False
    return True


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
    user_id = (
        data.get("userID")
        or data.get("user_id")
        or request.headers.get("userID")
        or request.headers.get("UserID")
    )

    if not verify_user(session_id, user_id):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    return None

@app.route('/listener', methods=['GET', 'POST'])
def sendMessage():
    auth_error = require_authenticated_user()
    if auth_error:
        return auth_error
    if request.method == 'POST':
        data = request.get_json()
        # Process incoming data
        return jsonify({"status": "received", "data": data}), 200
    
    return jsonify({"status": "listening"}), 200

@app.route('/listener/chat_history', methods=['GET'])
def requestChatHistory():
    auth_error = require_authenticated_user()
    if auth_error:
        return auth_error

    data = request.args
    data_dict = data.to_dict()
    roomID = data_dict["roomID"]
    messages = database.getMessages(roomID)

    return jsonify({"status": "chat history requested", "room_id": roomID,
                     "messages": [{"timestamp": time.time(), "message": message["content"],"senderID": message["senderID"]} for message in messages]}), 200

@app.route('/listener/chat_create', methods=['POST'])
def createChatRoomRequest():
    auth_error = require_authenticated_user()
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
    auth_error = require_authenticated_user()
    if auth_error:
        return auth_error

    data = request.get_json()
    data_dict = data.to_dict()
    try:
        room_id = data["roomID"]
        user_id = data["UserID"]
        response = _call_database("add_member", room_id, user_id)
        if response is None:
            return jsonify({"status": "error", "message": "Failed to invite user to chat room"}), 500

    except KeyError:
        return jsonify({"status": "error", "message": "Missing data in request data"}), 400
    return jsonify({"status": "user invited", "data": data}), 200

@app.route('/listener/get_user_id', methods=['POST'])
def getUserId():
    auth_error = require_authenticated_user()
    if auth_error:
        return auth_error

    data = request.get_json()
    data_dict = data.to_dict()
    try:
        username = data["username"]
        
        user_id = "user_" + username
        return jsonify({"status": "user found", "user_id": user_id}), 200

    except KeyError:
        return jsonify({"status": "error", "message": "Missing username in request data"}), 400

@app.route('/listener/chat_info', methods=['GET'])
def getChatRoomInfo():
    auth_error = require_authenticated_user()
    if auth_error:
        return auth_error

    data = request.args
    data_dict = data.to_dict()
    try:
        room_id = data_dict["roomID"]
        
        chat_info = {
            "room_id": room_id,
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)   

