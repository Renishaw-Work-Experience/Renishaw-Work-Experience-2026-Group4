from flask import Flask, request, jsonify
import time




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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)   

