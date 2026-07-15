import ttkbootstrap as ttk
import tkinter as tk

main = tk.Tk()
style = ttk.Style("flatly")
main.title("Chat User List")
main.geometry("400x320")


def resizeFonts(event):
    if event.widget == main:
        windowTitleFontSize = max(10, int(event.width * 0.022))
        windowTitleLabel.config(font=("Arial", windowTitleFontSize))


main.bind("<Configure>", resizeFonts)

userLists = ["User1", "User2", "User3", "User4", "User5", "User6", "User7", "User8", "User9", "User10"]

style.configure("windowTitleLabel.TLabel", background="#ffffff", foreground="#000000", font=("Arial", 15))
windowTitleLabel = ttk.Label(main, text="Chat User List", style="windowTitleLabel.TLabel")
windowTitleLabel.pack(pady=(10, 8))

style.configure("userListFrame.TFrame", background="#FFFFFF")
style.configure("userListUser.TLabel", background="#FFFFFF", foreground="#000000", font=("Arial", 12))

scroll_container = ttk.Frame(main)
scroll_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

canvas = tk.Canvas(scroll_container, highlightthickness=0, background="#f5f7fb")
canvas.pack(side="left", fill="both")

scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

content_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")


def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


content_frame.bind("<Configure>", on_frame_configure)

for user in userLists:
    userListFrame = ttk.Frame(content_frame, style="userListFrame.TFrame")
    userListFrame.pack(fill="x", pady=4)

    userListUser = ttk.Label(userListFrame, text=user, style="userListUser.TLabel")
    userListUser.pack(pady=6)


main.mainloop()