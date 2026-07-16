import customtkinter as ctk
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from database import database

dynList  = database.getDataByQuery("""
                                   SELECT AccountID, Username
                                   FROM Accounts""")

ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue") 

currentUser = {"Alice Smith": {"userId": "Id1", "password": "password1", "rooms": ["room1", "room2"]}}

userDetails = {
    "Alice Smith": {"userId": "Id1", "password": "password1", "rooms": ["room1", "room2"]},
    "Bob Jones": {"userId": "id2", "password": "password2", "rooms": ["room2"]},
    "Charlie Brown": {"userId": "id3", "password": "password3", "rooms": ["room3"]},
    "Diana Prince": {"userId": "id4", "password": "password4", "rooms": ["room4"]},
    "Evan Wright": {"userId": "id5", "password": "password5", "rooms": ["room5"]},
    "Fiona Gallagher": {"userId": "id6", "password": "password6", "rooms": ["room6"]}
}

dynNameList = list(userDetails.keys())
infoWindows = []
roomWindows = []

def startChat(userName, infoWindow, parentWindow):
    print(f"Starting chat with: {userName}")
    if infoWindow is not None:
        infoWindow.destroy()
    if parentWindow is not None:
        parentWindow.destroy()


def openRoom(roomID, infoWindow, parentWindow):
    print(f"Opening room: {roomID}")
    if infoWindow is not None:
        infoWindow.destroy()
    if parentWindow is not None:
        parentWindow.destroy()

def openUserInfo(userName, parent):
    global infoWindows

    for oldWindow in list(infoWindows):
        try:
            oldWindow.destroy()
        except Exception:
            pass
        if oldWindow in infoWindows:
            infoWindows.remove(oldWindow)

    userData = userDetails.get(userName, {"userId": "Unknown", "password": "No password set", "rooms": []})
    userId = userData.get("userId", "Unknown")
    password = userData.get("password", "No password set")
    rooms = userData.get("rooms", [])

    userInfoWindow = ctk.CTkToplevel(master=parent)
    userInfoWindow.title(f"Profile: {userName}")
    userInfoWindow.geometry("420x320")
    infoWindows.append(userInfoWindow)

    def onClose():
        if userInfoWindow in infoWindows:
            infoWindows.remove(userInfoWindow)
        userInfoWindow.destroy()


    userInfoWindow.protocol("WM_DELETE_WINDOW", onClose)

    userInfoWindowTitle = ctk.CTkLabel(userInfoWindow, text=f"Profile details for {userName}", font=("Segoe UI", 14, "bold"))
    userInfoWindowTitle.pack(padx=20, pady=(20, 10))

    userInfoWindowId = ctk.CTkLabel(userInfoWindow, text=f"User ID: {userId}", font=("Segoe UI", 12))
    userInfoWindowId.pack(padx=20, pady=(0, 5))


    contentFrame = ctk.CTkFrame(userInfoWindow)
    contentFrame.pack(fill="both", expand=True, padx=20, pady=20)

    userInfoWindowChatBtn = ctk.CTkButton(contentFrame, text="Start Chat", command=lambda: startChat(userName, userInfoWindow, parent))
    userInfoWindowChatBtn.pack(pady=(0, 10))

    userInfoWindowRoomLabel = ctk.CTkLabel(contentFrame, text="Available Chat Rooms:", font=("Segoe UI", 12))
    userInfoWindowRoomLabel.pack()

    for room in rooms:
        roomButton = ctk.CTkButton(contentFrame, text=room, command=lambda roomName=room: (print(f"Opening room: {roomName}"), (openRoom(roomName, userInfoWindow, parent))))
        roomButton.pack(pady=3)






class ContentCard(ctk.CTkFrame):
    def __init__(self, master, nameString, clickCallback):
        super().__init__(master, fg_color="#F2F2F2", corner_radius=8, border_width=1, border_color="#D1D1D1")
        
        self.avatar_lbl = ctk.CTkLabel(
            self, 
            text="👤", 
            font=("Segoe UI", 18),
            fg_color="#E0E0E0", 
            text_color="#333333",
            width=35,
            height=35,
            corner_radius=6
        )
        self.avatar_lbl.pack(side="left", padx=(15, 5), pady=10)
        
        self.name_btn = ctk.CTkButton(
            self, 
            text=nameString, 
            font=("Segoe UI", 14, "bold"),
            text_color="#1A1A1A",
            fg_color="transparent",
            hover_color="#E0E0E0",
            anchor="w",
            command=clickCallback
        )
        self.name_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

class chatUserListWindow(ctk.CTk):
    def __init__(self, dataSource):
        super().__init__()
        self.title("Dynamic Name Directory")
        self.geometry("400x450")

        # scrollbar
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=15)

        #show list
        self.render_cards(dataSource)

    def render_cards(self, nameList):
        for name in nameList:
            # asign name arg
            card = ContentCard(
                self.scroll_frame,
                nameString=name,
                clickCallback=lambda targetName=name: openUserInfo(targetName, self)
            )
            card.pack(fill="x", pady=5, padx=5)


ChatUserListWindow = chatUserListWindow(dataSource=dynNameList)
ChatUserListWindow.mainloop()
