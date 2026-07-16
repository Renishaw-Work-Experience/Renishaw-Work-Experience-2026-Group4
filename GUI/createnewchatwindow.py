import customtkinter
from PIL import Image
import os
import sys
from pathlib import Path
import chatinterface2 as chatinterface

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
from client import sender



script_dir = os.path.dirname(os.path.abspath(__file__))

groupchatusernameentries = []



def addnewperson():
    entry = customtkinter.CTkEntry(personlistframe, placeholder_text="Enter persons username", height=50, width=400, fg_color="white", text_color="darkblue")
    entry.pack(pady=5)
    groupchatusernameentries.append(entry)

def createnewchat():
    userIDs = []
    session = chatinterface.getSession()
    invalidUsernamesIdx = []
    usernames = []
    for idx, username in enumerate(groupchatusernameentries):
        userID = sender.ID_from_username(username)
        if userID:
            userIDs.append(userID)
            usernames.append(username)
        else:
            invalidUsernamesIdx.append(idx)
    invalidUsernamesIdx.reverse()
    for i in invalidUsernamesIdx:
        username.pop(i)
    usernames.append(sender.usernameFromID(session.userID))
    userIDs.append(session.senderID)
    

    chatname = chatnameentry.get()


    session.createChatRoom(chatname, userIDs)


    print(chatname)
    

    sys.exit()

app = customtkinter.CTk()
app.geometry("600x400")
app.title("Chat creation")

titlefont = customtkinter.CTkFont(size=30)
title = customtkinter.CTkLabel(app, text="Create a new chat", font=titlefont)
title.place(relx=0.1, rely=0.05)

personlistframe = customtkinter.CTkScrollableFrame(app, fg_color="grey55")
personlistframe.place(relx=0.1,rely=0.3,relwidth=0.6,relheight=0.4)

chatnameentry = customtkinter.CTkEntry(app, fg_color="grey90", placeholder_text="Enter chat title", text_color="darkblue")
chatnameentry.place(relx=0.1,rely=0.18, relwidth=0.4, relheight=0.1)

addpersonbutton = customtkinter.CTkButton(app, text="Add another person", command=addnewperson)
addpersonbutton.place(relx=0.7,rely=0.3,relwidth=0.25,relheight=0.1)

addnewperson()

createchat = customtkinter.CTkButton(app, text="Create new chat", command=createnewchat)
createchat.place(relwidth=0.4, relheight=0.1, relx=0.3, rely=0.8)

app.mainloop()