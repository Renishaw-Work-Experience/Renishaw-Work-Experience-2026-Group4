import customtkinter
from PIL import Image
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

def addnewperson():
    customtkinter.CTkEntry(personlistframe, placeholder_text="Enter persons username", height=50, width=400, fg_color="white").pack(pady=5)

app = customtkinter.CTk()
app.geometry("600x400")
app.title("Chat creation")

titlefont = customtkinter.CTkFont(size=30)
title = customtkinter.CTkLabel(app, text="Create a new chat", font=titlefont)
title.place(relx=0.1, rely=0.05)

personlistframe = customtkinter.CTkScrollableFrame(app, fg_color="grey55")
personlistframe.place(relx=0.1,rely=0.2,relwidth=0.6,relheight=0.5)

addpersonbutton = customtkinter.CTkButton(app, text="Add another person", command=addnewperson)
addpersonbutton.place(relx=0.7,rely=0.2,relwidth=0.25,relheight=0.1)

person1 = customtkinter.CTkEntry(personlistframe, placeholder_text="Enter persons username", height=50, width=400, fg_color="white")
person1.pack(pady=5)

createchat = customtkinter.CTkButton(app, text="Create new chat")
createchat.place(relwidth=0.4, relheight=0.1, relx=0.3, rely=0.8)

app.mainloop()