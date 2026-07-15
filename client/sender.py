import requests
import time

address = "http://127.0.0.1:5000"
send_listener = "/listener"
request_chat_history_listener = "/listener/chat_history"

#RoomID, message, senderID, receiverID, timestamp added in function
def login( username, password):
    try:
        login_data = {"username": username, "password": password}
        response = requests.post(address + "/listener/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print("Login successful:", data)
            return session(data.get("user_id"), data.get("session_id"))
        else:
            print("Failed to login. Status code:", response.status_code)
            return None
    except Exception as e:
        print("Error during login:", e)
        return None
    
def signup( username, password):
    try:
        signup_data = {"username": username, "password": password}
        response = requests.post(address + "/listener/signup", json=signup_data)
        if response.status_code in [200, 201]:
            data = response.json()
            print("Signup successful:", data)
            return None
        else:
            print("Failed to signup. Status code:", response.status_code)
            return None
    except Exception as e:
        print("Error during signup:", e)
        return None


class session:
    def __init__(self,senderID,sessionID):
        self.senderID, self.sessionID = senderID,sessionID
        

    def sendMessage(self,data,roomID):
        try:
            send_data = {"message":data}
            send_data["timestamp"] = time.time()
            send_data["senderID"] = self.senderID
            send_data["roomID"] = roomID
            send_data["sessionID"] = self.sessionID
            response = requests.post(address + send_listener, json=send_data)
            if response.status_code == 200:
                print("Data sent successfully:", response.json())
            else:
                print("Failed to send data. Status code:", response.status_code)
        except Exception as e:
            print("Error sending data:", e)

    def requestChatHistory(self, room_id):
        try:
            response = requests.get(address + request_chat_history_listener, params={"RoomID": room_id})
            if response.status_code == 200:
                print("Chat history received:", response.json())
                return(response["messages"])
            else:
                #{"status": "chat history requested", "room_id": RoomID,
                #"messages": [{"timestamp": time.time(), "message": "Sample message","senderID": "user1"}]}), 200

                print("Failed to retrieve chat history. Status code:", response.status_code)
                return  [{"timestamp": time.time(), "message": "Failed to retrieve chat history. ","senderID": "system"}]
        except Exception as e:
            print("Error retrieving chat history:", e)

    def inviteToChat(self, room_id, user_id):
        try:
            invite_data = {"RoomID": room_id, "UserID": user_id, "senderID":self.senderID}
            response = requests.post(address + "/listener/chat_invite", json=invite_data)
            if response.status_code == 200:
                print("User invited successfully:", response.json())
            else:
                print("Failed to invite user. Status code:", response.status_code)
        except Exception as e:
            print("Error inviting user:", e)

    def createChatRoom(self, name, members):
        try:
            create_data = {"name": name, "members": members, "senderID": self.senderID,"sessionID": self.sessionID}
            response = requests.post(address + "/listener/chat_create", json=create_data)
            if response.status_code == 200:
                print("Chat room created successfully:", response.json())
            else:
                print("Failed to create chat room. Status code:", response.status_code)
        except Exception as e:
            print("Error creating chat room:", e)

    def getChatRoomInfo(self, room_id):
        try:
            response = requests.get(address + "/listener/chat_info", params={"RoomID": room_id})
            if response.status_code == 200:
                print("Chat room info received:", response.json())
                return response["chat_info"]
            else:
                print("Failed to retrieve chat room info. Status code:", response.status_code)
        except Exception as e:
            print("Error retrieving chat room info:", e)

    def getRoomsFromUserID(self):
        request = {"timestamp":time.time(),"userID":self.senderID,"sessionID":self.sessionID}
        response = requests.get(address+'/listener/roomMembership',json=request)
        if response.status_code == 200:
            print("getting chat rooms successful")
        else:
            print("getting chat rooms unsuccessful")


   

def ID_from_username(username):
    data = {"username": username}
    response = requests.get(address + "/listener/get_user_id", json=data)
    if response.status_code == 200:
        return response.json().get("user_id")
    elif response.status_code == 404:
        print("User not found.")
        print("Failed to retrieve user ID. Status code:", response.status_code)
        return None
    else:
        print("Failed to retrieve user ID. Status code:", response.status_code)
        return None

def usernameFromID(ID):
    data = {"userID":ID}
    response = requests.get(address + "/listener/get_username", json=data)
    if response.status_code == 200:
        return response.json().get("username")
    elif response.status_code == 404:
        print("User not found.")
        print("Failed to retrieve username. Status code:", response.status_code)
        return None
    else:
        print("Failed to retrieve username. Status code:", response.status_code)
        return None



if __name__ == "__main__":
    session = session("user1")
    session.sendMessage({"message": "Hello, server!"})


    session.createChatRoom("MyChatRoom", ["user1", "user2"])
    session.inviteToChat("MyChatRoom", "user3")


    session.requestChatHistory("MyChatRoom")