import customtkinter 
from PIL import Image
import os
from pathlib import Path
import sys 

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
from ..client import sender

# ensure image paths work regardless of current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))

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

sendimage = customtkinter.CTkImage(light_image=Image.open(os.path.join(script_dir, "send_button.png")), size=(50,50))

newchatimage = customtkinter.CTkImage(light_image=Image.open(os.path.join(script_dir, "new_chat.png")), size=(50,50))
newchatlabel = customtkinter.CTkButton(chatroomsframe, image=newchatimage, text="", corner_radius=50, fg_color="deep sky blue")
newchatlabel.place(relx=0.6,rely=0.22, relwidth=0.3, relheight=0.5)

chatnamefont = customtkinter.CTkFont(size=25)
chatnamelabel = customtkinter.CTkLabel(chatnameframe, text=chatname, font=chatnamefont)
chatnamelabel.place(relx=0.03,rely=0.25)

chatcontent = customtkinter.CTkScrollableFrame(app, fg_color="grey87")
chatcontent.place(relx=0.27,rely=0.15, relwidth=0.71, relheight=0.65)

messageinputbox = customtkinter.CTkTextbox(app, fg_color="grey60", corner_radius=20)
messageinputbox.place(relx=0.27, rely=0.82, relwidth=0.6, relheight=0.15)

def send_message():
    message = messageinputbox.get()
    sender.



sendimage = customtkinter.CTkImage(light_image=Image.open(os.path.join(script_dir, "send_button.png")), size=(50,50))
sendbtn = customtkinter.CTkButton(app, image=sendimage, text="", fg_color="deep sky blue", corner_radius=50,command=send_message)
sendbtn.place(relx=0.89, rely=0.84, relwidth=0.07, relheight=0.11)

def main(session):
    app.mainloop()

if __name__ == "__main__":
    app.mainloop()