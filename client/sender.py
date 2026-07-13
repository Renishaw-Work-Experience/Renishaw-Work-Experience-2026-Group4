import requests
import time

address = "http://127.0.0.1:5000"
send_listener = "/listener"
request_chat_history_listener = "/listener/chat_history"

#RoomID, message, senderID, receiverID, timestamp added in function
class session:
    def __init__(self,senderID):
        self.senderID = senderID

    def send_message(self,data):
        try:
            send_data = data
            send_data["timestamp"] = time.time()
            send_data["senderID"] = self.senderID
            response = requests.post(address + send_listener, json=send_data)
            if response.status_code == 200:
                print("Data sent successfully:", response.json())
            else:
                print("Failed to send data. Status code:", response.status_code)
        except Exception as e:
            print("Error sending data:", e)

    def request_chat_history(self, room_id):
        try:
            response = requests.get(address + request_chat_history_listener, params={"RoomID": room_id})
            if response.status_code == 200:
                print("Chat history received:", response.json())
            else:
                print("Failed to retrieve chat history. Status code:", response.status_code)
        except Exception as e:
            print("Error retrieving chat history:", e)


session = session("user1")
session.send_message({"message": "Hello, server!"})

session.request_chat_history("room123")