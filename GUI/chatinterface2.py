import customtkinter 
from PIL import Image
import os

# ensure image paths work regardless of current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))

messagelist = [{"timestamp":2375758535, "message":"hellothisisatestmessagetodisplay", "senderid":234}, {"timestamp":34587345983, "message":"another mdfgiuherfuivhbevuyebvuyfbviubyifuvbfdiubveiuvbdfivubeiuvbeiuvbdfiuvbfdiuvbsiuvbfdiuvberiuvbreiuvbreiubvfsiuvbsdfiuvbdfiuvbfdiuvbdfiuvbfdeviubdfessage", "senderid":233345345348954},{"timestamp":34587345983, "message":"another message", "senderid":234353454338954},{"timestamp":34587345983, "message":"another message", "senderid":23334534348954},{"timestamp":34587345983, "message":"another message", "senderid":2335464538954},{"timestamp":34587345983, "message":"another message", "senderid":233895546454},{"timestamp":3458732343245983, "message":"another message", "senderid":345345},{"timestamp":43534534, "message":"another message", "senderid":345345},{"timestamp":34587345983, "message":"another message", "senderid":34543}]

def loadchats(messages):
    for widget in chatcontent.winfo_children():
        widget.destroy()
    for message in messages:
        x = message["message"]
        useridformessage = message["senderid"]
        messagedisplay = customtkinter.CTkLabel(chatcontent, fg_color="grey56", text=(f"{useridformessage}: {x}"), corner_radius=10, justify="left", anchor="w", wraplength=500)
        messagedisplay.pack(padx=5, pady=5, anchor="w")

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

newchatimage = customtkinter.CTkImage(light_image=Image.open(os.path.join(script_dir, "new_chat.png")), size=(50,50))
newchatlabel = customtkinter.CTkButton(chatroomsframe, image=newchatimage, text="", corner_radius=50, fg_color="deep sky blue")
newchatlabel.place(relx=0.6,rely=0.22, relwidth=0.3, relheight=0.6)

chatnamefont = customtkinter.CTkFont(size=25)
chatnamelabel = customtkinter.CTkLabel(chatnameframe, text=chatname, font=chatnamefont)
chatnamelabel.place(relx=0.03,rely=0.25)

chatcontent = customtkinter.CTkScrollableFrame(app, fg_color="grey87")
chatcontent.place(relx=0.27,rely=0.15, relwidth=0.71, relheight=0.65)

messageinputbox = customtkinter.CTkTextbox(app, fg_color="grey60", corner_radius=20)
messageinputbox.place(relx=0.27, rely=0.82, relwidth=0.6, relheight=0.15)

sendimage = customtkinter.CTkImage(light_image=Image.open(os.path.join(script_dir, "send_button.png")), size=(50,50))
sendbtn = customtkinter.CTkButton(app, image=sendimage, text="", fg_color="deep sky blue", corner_radius=50)
sendbtn.place(relx=0.89, rely=0.84, relwidth=0.07, relheight=0.11)

testchat = customtkinter.CTkButton(listofchatsframe, text=chatname, fg_color="blue", height=30, width=200, command=lambda:loadchats(messagelist))
testchat.pack()

app.mainloop()