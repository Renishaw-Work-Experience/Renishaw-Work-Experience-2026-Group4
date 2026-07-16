import threading
import customtkinter 
from PIL import Image
import os
from pathlib import Path
import sys 
import subprocess


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
from client import sender

# ensure image paths work regardless of current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# messagelist = [{"timestamp":2375758535, "message":"hellothisisatestmessagetodisplay", "senderid":234}, {"timestamp":34587345983, "message":"another mdfgiuherfuivhbevuyebvuyfbviubyifuvbfdiubveiuvbdfivubeiuvbeiuvbdfiuvbfdiuvbsiuvbfdiuvberiuvbreiuvbreiubvfsiuvbsdfiuvbdfiuvbfdiuvbdfiuvbfdeviubdfessage", "senderid":233345345348954},{"timestamp":34587345983, "message":"another message", "senderid":234353454338954},{"timestamp":34587345983, "message":"another message", "senderid":23334534348954},{"timestamp":34587345983, "message":"another message", "senderid":2335464538954},{"timestamp":34587345983, "message":"another message", "senderid":233895546454},{"timestamp":3458732343245983, "message":"another message", "senderid":345345},{"timestamp":43534534, "message":"another message", "senderid":345345},{"timestamp":34587345983, "message":"another message", "senderid":34543}]
try:
    print(session)
except NameError:
    session = None

def set_session(s):
    global session
    session = s
    
def getSession():
    return session
chatRoomButtons = []


def start_app():
    """Create and run the chat UI. Call this after successful login."""
    app = customtkinter.CTk()
    app.geometry("1000x600")
    app.title("Chat messaging service")

    def loadchats(messages, room, label):
        nonlocal currentRoomID
        chatname = room["name"]
        currentRoomID = room["roomID"]
        notificationChatroom(room["roomID"], False)
        label.configure(text=chatname)
        for widget in chatcontent.winfo_children():
            widget.destroy()
        for message in messages:
            x = message["message"]
            useridformessage = message["senderID"]
            messagedisplay = customtkinter.CTkLabel(chatcontent, fg_color="grey56", text=(f"{useridformessage}: {x}"), corner_radius=10, justify="left", anchor="w", wraplength=500)
            messagedisplay.pack(padx=5, pady=5, anchor="w")

    def getChatRooms(): # Collect the chat rooms from the server
        #chatroomlist = [{"roomID":1, "name":"testname", "user1ID":1, "user2ID":2, "user3ID":None, "user4ID":None, "user5ID":None},{"roomID":2, "name":"ADifferentTestName", "user1ID":1, "user2ID":2, "user3ID":None, "user4ID":None, "user5ID":None}]
        response = session.getRoomsFromUserID()
        if not response:
            return
        chatroomlist = response
        print(chatroomlist)
        return chatroomlist
        # PLACEHOLDER!!!

    def getChatHistory(roomID): # Collect the chat history from the server
        print("Getting history for room", roomID)
        """
        if roomID == 1:
            messagelist = [{"timestamp":2375758535, "message":"hellothisisatestmessagetodisplay", "senderid":234}, {"timestamp":34587345983, "message":"another mdfgiuherfuivhbevuyebvuyfbviubyifuvbfdiubveiuvbdfivubeiuvbeiuvbdfiuvbfdiuvbsiuvbfdiuvberiuvbreiuvbreiubvfsiuvbsdfiuvbdfiuvbfdiuvbdfiuvbfdeviubdfessage", "senderid":233345345348954},{"timestamp":34587345983, "message":"another message", "senderid":234353454338954},{"timestamp":34587345983, "message":"another message", "senderid":23334534348954},{"timestamp":34587345983, "message":"another message", "senderid":2335464538954},{"timestamp":34587345983, "message":"another message", "senderid":233895546454},{"timestamp":3458732343245983, "message":"another message", "senderid":345345},{"timestamp":43534534, "message":"another message", "senderid":345345},{"timestamp":34587345983, "message":"another message", "senderid":34543}]
        elif roomID == 2:
            messagelist = [{"timestamp":2375758535, "message":"A different message", "senderid":111}, {"timestamp":34587345983, "message":"bonjour", "senderid":222},{"timestamp":34587345983, "message":"WAHOOOO", "senderid":384}]
        else:
            messagelist = [{"timestamp":2375758535, "message":"No messages in this chat room", "senderid":0}]
        # ^ This is placeholder for now. We will request from the server
        """
        
        return session.requestChatHistory(roomID)

    def convertRoomsToButtons(userID, label):
        chatrooms = getChatRooms()
        if not chatrooms:
            return
        for room in chatrooms:
            print("room:",room["name"])
            roomname = room["name"]
            roomID = room["roomID"]
            print(f"Room name: {roomname}, Room ID: {roomID}")
            chatbutton = customtkinter.CTkButton(listofchatsframe, text=roomname, fg_color="blue", height=30, width=200, command=lambda room=room:loadchats(getChatHistory(room["roomID"]), room, label))
            chatbutton.room = room
            chatbutton.pack(pady=5)
            global chatRoomButtons
            chatRoomButtons.append(chatbutton)
            print(chatRoomButtons)

    def findChatButton(chatRoomID):
        global chatRoomButtons
        for button in chatRoomButtons:
            if button.room["roomID"] == chatRoomID:
                return button
            
    def notificationChatroom(chatRoomID, hasNotification : bool):
        if hasNotification:
            button = findChatButton(chatRoomID)
            if button:
                button.configure(fg_color="red")
        else:
            button = findChatButton(chatRoomID)
            if button:
                button.configure(fg_color="blue")

    


    chatroomsframe = customtkinter.CTkFrame(app, corner_radius=20, fg_color="dodger blue")
    chatroomsframe.place(relx=0.0,rely=0.0, relwidth=0.25, relheight=0.15, anchor="nw")

    chatname = "testname"

    chatroomsframe = customtkinter.CTkFrame(app, corner_radius=20, fg_color="dodger blue")
    chatroomsframe.place(relx=0.0,rely=0.0, relwidth=0.25, relheight=0.15, anchor="nw")

    titlefont = customtkinter.CTkFont(size=30, weight="bold")
    chatroomsframetext = customtkinter.CTkLabel(chatroomsframe, text="Chats", font=titlefont, text_color="black")
    chatroomsframetext.place(relx=0.1, rely=0.3)

    listofchatsframe = customtkinter.CTkScrollableFrame(app, corner_radius=20, fg_color="grey")
    listofchatsframe.place(relx=0.0,rely=0.15, relwidth=0.25, relheight=0.85, anchor="nw")

    chatnameframe = customtkinter.CTkFrame(app, corner_radius=10, fg_color="dodger blue")
    chatnameframe.place(relx=0.27, rely=0.03, relwidth= 0.71, relheight=0.10, anchor="nw")
    def createChatRoom():
        process = subprocess.Popen([sys.executable, os.path.join(script_dir, "createnewchatwindow.py")])
    
    def showChatInfo():
        pass
        # process = subprocess.Popen([sys.executable, os.path.join(script_dir, "chatUserListWindow.py")]) # TODO: CHANGE FILENAME

    

    

    app.grid_columnconfigure(0,weight=1)
    app.grid_rowconfigure(0,weight=1)

    # load images (wrap in try/except to avoid crashing if missing during import)
    try:
        send_img = Image.open(os.path.join(script_dir, "send_button.png"))
    except Exception:
        send_img = None

    try:
        new_chat_img = Image.open(os.path.join(script_dir, "new_chat.png"))
    except Exception:
        new_chat_img = None

    try:
        info_img = Image.open(os.path.join(script_dir, "info.png"))
    except Exception:
        info_img = None

    infoimage = customtkinter.CTkImage(light_image=info_img, size=(40, 40)) if info_img else None
    chatinfobtn = customtkinter.CTkButton(chatnameframe, image=infoimage, text="", fg_color="blue", command=lambda:showChatInfo(), width=50, height=50)
    chatinfobtn.place(relx=0.9, rely=0.09)

    newchatimage = customtkinter.CTkImage(light_image=new_chat_img, size=(50,50)) if new_chat_img else None
    newchatlabel = customtkinter.CTkButton(chatroomsframe, image=newchatimage, text="", corner_radius=50, fg_color="deep sky blue", command=lambda:createChatRoom())
    newchatlabel.place(relx=0.6,rely=0.22, relwidth=0.3, relheight=0.5)

    chatnamefont = customtkinter.CTkFont(size=25)
    chatnamelabel = customtkinter.CTkLabel(chatnameframe, text=chatname, font=chatnamefont)
    chatnamelabel.place(relx=0.03,rely=0.25)

    chatcontent = customtkinter.CTkScrollableFrame(app, fg_color="grey87")
    chatcontent.place(relx=0.27,rely=0.15, relwidth=0.71, relheight=0.65)

    messageinputbox = customtkinter.CTkTextbox(app, fg_color="grey60", corner_radius=20)
    messageinputbox.place(relx=0.27, rely=0.82, relwidth=0.6, relheight=0.15)

    currentRoomID = ""

    chatnamefont = customtkinter.CTkFont(size=25)
    chatnamelabel = customtkinter.CTkLabel(chatnameframe, text="Open Chat...", font=chatnamefont)
    chatnamelabel.place(relx=0.03,rely=0.25)

    def sendMessage():
        message = messageinputbox.get("0.0", "end").strip()
        global session
        if session is None:
            print("No session set - cannot send message")
            return
        if not message:
            print("No message to send")
            return
        try:
            session.sendMessage(message, currentRoomID)
        except Exception as e:
            print("Failed to send message:", e)

    sendimage = customtkinter.CTkImage(light_image=send_img, size=(50,50)) if send_img else None
    sendbtn = customtkinter.CTkButton(app, image=sendimage, text="", fg_color="deep sky blue", corner_radius=50,command=sendMessage)
    sendbtn.place(relx=0.89, rely=0.84, relwidth=0.07, relheight=0.11)

    convertRoomsToButtons(session.senderID, chatnamelabel)


    print(chatRoomButtons)
    notificationChatroom(1, True)
    
    def printit():
        threading.Timer(1, printit).start()
        messages = sender.getAllMessages()
        print("Messages received:", messages)
        for widget in chatcontent.winfo_children():
            widget.destroy()
        for message in messages:
            x = message["content"]
            useridformessage = message["senderID"]
            messagedisplay = customtkinter.CTkLabel(chatcontent, fg_color="grey56", text=(f"{useridformessage}: {x}"), corner_radius=10, justify="left", anchor="w", wraplength=500)
            messagedisplay.pack(padx=5, pady=5, anchor="w")
    printit()
    app.mainloop()


    

if __name__ == "__main__":
    start_app()
