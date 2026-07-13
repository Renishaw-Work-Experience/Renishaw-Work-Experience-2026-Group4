from flask import Flask, request, jsonify
import time
import database



app = Flask(__name__)

@app.route('/listener', methods=['GET', 'POST'])
def listen():
    if request.method == 'POST':
        data = request.get_json()
        # Process incoming data
        return jsonify({"status": "received", "data": data}), 200
    
    return jsonify({"status": "listening"}), 200

@app.route('/listener/chat_history', methods=['GET'])
def request_chat_history():
    data = request.args
    data_dict = data.to_dict()
    RoomID = data_dict["RoomID"]

    return jsonify({"status": "chat history requested", "room_id": RoomID,
                     "messages": [{"timestamp": time.time(), "message": "Sample message","senderID": "user1"}]}), 200

@app.route('/listener/chat_create', methods=['POST'])
def create_chat_room_request():
    data = request.get_json()
    data_dict = data.to_dict()
    try:
        name = data_dict["name"]
        members = data_dict["members"]
        group_id = name + "_" + data_dict["sender"] + "_" + str(int(time.time()))
        response = database.create_chat_room(name, members, data_dict["sender"])
        if response is None:
            return jsonify({"status": "error", "message": "Failed to create chat room"}), 500

    except KeyError:
        return jsonify({"status": "error", "message": "Missing data in request data"}), 400
    return jsonify({"status": "chat created", "data": data}), 200

@app.route('/listener/chat_invite', methods=['POST'])
def invite_to_chat():
    data = request.get_json()
    data_dict = data.to_dict()
    try:
        room_id = data_dict["RoomID"]
        user_id = data_dict["UserID"]
        response = database.add_member(room_id, user_id)
        if response is None:
            return jsonify({"status": "error", "message": "Failed to invite user to chat room"}), 500

    except KeyError:
        return jsonify({"status": "error", "message": "Missing data in request data"}), 400
    return jsonify({"status": "user invited", "data": data}), 200

@app.route('/listener/get_user_id', methods=['POST'])
def get_user_id():
    data = request.get_json()
    data_dict = data.to_dict()
    try:
        username = data_dict["username"]
        
        user_id = "user_" + username
        return jsonify({"status": "user found", "user_id": user_id}), 200

    except KeyError:
        return jsonify({"status": "error", "message": "Missing username in request data"}), 400

@app.route('/listener/chat_info', methods=['GET'])
def get_chat_room_info():
    data = request.args
    data_dict = data.to_dict()
    try:
        room_id = data_dict["RoomID"]
        
        chat_info = {
            "room_id": room_id,
            "name": "Sample Chat Room",
            "members": ["user1", "user2", "user3"],
            "created_at": time.time()
        }
        return jsonify({"status": "chat info retrieved", "chat_info": chat_info}), 200

    except KeyError:
        return jsonify({"status": "error", "message": "Missing RoomID in request data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)   

