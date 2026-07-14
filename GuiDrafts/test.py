import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import customtkinter as ctk

main =tk.Tk()

style = Style("darkly") #theme
main.title('GUI App')
main.geometry('500x500')

chatroomName = "testRoom"

def resize_fonts(event):
    #init when window resize
    if event.widget == main:
        #calc window width rel
        listHeaderBoxFontSize = max(10, int(event.width * 0.024))
        chatroomHeaderBoxFontSize = max(8, int(event.width * 0.022))
        
        # upd font size
        style.configure("chatroomListHeader.TLabel", font=('Arial', listHeaderBoxFontSize))
        style.configure("chatroomHeader.TLabel", font=('Arial', chatroomHeaderBoxFontSize))

# Bind resize to main window                                 ⌄⌄⌄⌄⌄⌄
main.bind("<Configure>", resize_fonts)#0 idea but power of >>GOOGLE<<
#                                                            ^^^^^^        
 
chatroomListContentBoxColor = "#39A1FB"
style.configure("chatroomListContentBox.TFrame", background=chatroomListContentBoxColor)
chatroomListContentBox = ttk.Frame(main, style="chatroomListContentBox.TFrame")
chatroomListContentBox.place(relx=0.0, rely=0.1, relwidth=0.2, relheight=0.9, anchor='nw')                                                

listHeaderBoxColor = "#0080FF" #dark blue
style.configure("chatroomListHeaderBox.TFrame", background=listHeaderBoxColor)
chatroomListHeaderBox = ttk.Frame(main, style="chatroomListHeaderBox.TFrame")
chatroomListHeaderBox.place(relx=0.0, rely=0.0, relwidth=0.2, relheight=0.1, anchor='nw')

style.configure("chatroomListHeader.TLabel", background=listHeaderBoxColor, foreground="white")
chatroomsListHeader = ttk.Label(chatroomListHeaderBox, text='Chatrooms', style="chatroomListHeader.TLabel" )
chatroomsListHeader.place(relx=0.01, rely=0.2, anchor='nw')

# chatroomHeaderBoxColor = "#0080FF"
# style.configure("chatroomHeaderBox.TFrame", background=chatroomHeaderBoxColor)
# chatroomHeaderBox = ttk.Frame(main, style="chatroomHeaderBox.TFrame")
# chatroomHeaderBox.place(relx=0.2, rely=0.0, relwidth=0.95, relheight=0.1, anchor="nw")

# style.configure("chatroomHeader.TLabel", background=chatroomHeaderBoxColor,foreground="white")
# chatroomHeader = ttk.Label(chatroomHeaderBox, text=chatroomName, style="chatroomHeader.TLabel")
# chatroomHeader.place(relx=0.5, rely=0.0, anchor='nw')

# chatroomContentBox = "#03274C"
# style.configure("messageHistoryBox.TFrame", background=chatroomContentBox)
# chatroomContentBox = ttk.Frame(main, style="chatroomContentBox.TFrame")
# chatroomContentBox.place(relx=0.2, rely=0.1, relwidth=0.8, relheight=0.9)

# messageInputFieldColor = "#004B97"
# messageInputField = ctk.CTkTextbox(main, border_width=1, corner_radius=15, bg_color=chatroomContentBox,fg_color=messageInputFieldColor)
# messageInputField.place(relx=0.225, rely=0.75, relwidth=0.709, relheight=0.2, anchor='nw')
# messageInputField._textbox.configure(highlightthickness=0, borderwidth=0)


# submitMessageBtnC
# submitMessageBtn = ttk.Button=(chatroomContentBox)
# submitMessageBtn.place()

# button1 = ttk.Button(text='Button1', bootstyle="info")
# button1.pack()

# button2 = ttk.Button(text='Button2', bootstyle="success")
# button2.pack()

# button3 = ttk.Button(text='Button3', bootstyle="warning")
# button3.pack()

main.mainloop()
