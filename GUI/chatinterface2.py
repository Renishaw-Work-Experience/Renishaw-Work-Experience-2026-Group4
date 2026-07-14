import customtkinter 
from PIL import Image
import os
from pathlib import Path
import sys 

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
from client import sender

# ensure image paths work regardless of current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# module-level session object (set by loginPageInterface)
session = None

def set_session(s):
    global session
    session = s

def start_app():
    """Create and run the chat UI. Call this after successful login."""
    app = customtkinter.CTk()
    app.geometry("1000x600")
    app.title("Chat messaging service")

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

    newchatimage = customtkinter.CTkImage(light_image=new_chat_img, size=(50,50)) if new_chat_img else None
    newchatlabel = customtkinter.CTkButton(chatroomsframe, image=newchatimage, text="", corner_radius=50, fg_color="deep sky blue")
    newchatlabel.place(relx=0.6,rely=0.22, relwidth=0.3, relheight=0.5)

    chatnamefont = customtkinter.CTkFont(size=25)
    chatnamelabel = customtkinter.CTkLabel(chatnameframe, text=chatname, font=chatnamefont)
    chatnamelabel.place(relx=0.03,rely=0.25)

    chatcontent = customtkinter.CTkScrollableFrame(app, fg_color="grey87")
    chatcontent.place(relx=0.27,rely=0.15, relwidth=0.71, relheight=0.65)

    messageinputbox = customtkinter.CTkTextbox(app, fg_color="grey60", corner_radius=20)
    messageinputbox.place(relx=0.27, rely=0.82, relwidth=0.6, relheight=0.15)

    def sendMessage():
        message = messageinputbox.get("0.0", "end").strip()
        global session
        if session is None:
            print("No session set - cannot send message")
            return
        try:
            session.send_message(message)
        except Exception as e:
            print("Failed to send message:", e)

    sendimage = customtkinter.CTkImage(light_image=send_img, size=(50,50)) if send_img else None
    sendbtn = customtkinter.CTkButton(app, image=sendimage, text="", fg_color="deep sky blue", corner_radius=50,command=sendMessage)
    sendbtn.place(relx=0.89, rely=0.84, relwidth=0.07, relheight=0.11)

    app.mainloop()


if __name__ == "__main__":
    start_app()