import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import customtkinter as ctk
import sys
from pathlib import Path
import chatinterface2

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from client import sender

main = tk.Tk()

style = Style("flatly")
main.title("GUI App")
main.geometry("500x500")
main.configure(bg="#f5f7fb")

chatroomName = "testRoom"


def resize_fonts(event):
    if event.widget == main:
        loginPageTitle = max(10, int(event.width * 0.024))
        userPasswordInputLabelScale = max(8, int(event.width * 0.022))
        usernameInputLabelScale = max(8, int(event.width * 0.022))

        style.configure("userPasswordInputLabel.TLabel", font=("Arial", userPasswordInputLabelScale))
        style.configure("loginPageTitle.TLabel", font=("Arial", loginPageTitle))
        style.configure("usernameInputLabel.TLabel", font=("Arial", usernameInputLabelScale))


main.bind("<Configure>", resize_fonts)

pageBackgroundColor = "#f5f7fb"
main.configure(background=pageBackgroundColor)

loginPageTitleBoxColor = pageBackgroundColor
style.configure("loginPageTitleBox.TFrame", background=loginPageTitleBoxColor)
loginPageTitleBox = ttk.Frame(main, style="loginPageTitleBox.TFrame")
loginPageTitleBox.place(relx=0.25, rely=0.0, relwidth=0.5, relheight=0.2, anchor="w")

style.configure("loginPageTitle.TLabel", background=pageBackgroundColor, foreground="#1f2937")
loginPageTitle = ttk.Label(main, text="Login Page", style="loginPageTitle.TLabel")
loginPageTitle.place(relx=0.5, rely=0.0, anchor="n")

inputFieldxPos = 0.6
inputFieldWidth = 0.3
inputFieldHeight = 0.1
inputFieldColor = "#ffffff"

style.configure("usernameInputLabel.TLabel", background=pageBackgroundColor, foreground="#374151")
usernameInputLabel = ttk.Label(main, text="Username", style="usernameInputLabel.TLabel")
usernameInputLabel.place(relx=0.4, rely=0.2, anchor="n")

usernameInputField = ctk.CTkEntry(main, border_width=1, corner_radius=15, bg_color=pageBackgroundColor, fg_color=inputFieldColor, text_color="#111827")
usernameInputField.place(relx=inputFieldxPos, rely=0.2, relwidth=inputFieldWidth, relheight=inputFieldHeight, anchor="nw")

style.configure("userPasswordInputLabel.TLabel", background=pageBackgroundColor, foreground="#374151")
userPasswordInputLabel = ttk.Label(main, text="Password", style="userPasswordInputLabel.TLabel")
userPasswordInputLabel.place(relx=0.4, rely=0.4, anchor="n")

userPasswordInputField = ctk.CTkEntry(main, border_width=1, corner_radius=15, bg_color=pageBackgroundColor, fg_color=inputFieldColor, text_color="#111827")
userPasswordInputField.place(relx=inputFieldxPos, rely=0.4, relwidth=inputFieldWidth, relheight=inputFieldHeight, anchor="nw")


def userSubmitData():
    username = usernameInputField.get()
    password = userPasswordInputField.get()
    session = sender.login(username,password)
    #session = True #test
    if session == None:
        return
        #do something when login fails
    else:
        # close the login window, then open the chat interface
        try:
            main.destroy()
        except Exception:
            pass
        chatinterface2.app.mainloop()


    print(f"Username: {username}")
    print(f"Password: {password}")


userSubmitDataBtn = ctk.CTkButton(main, text="Submit", command=userSubmitData, fg_color="#4f46e5", hover_color="#4338ca", text_color="white")
userSubmitDataBtn.place(relx=0.1, rely=0.6, anchor="n")

main.mainloop()
