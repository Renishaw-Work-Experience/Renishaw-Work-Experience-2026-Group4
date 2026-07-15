import customtkinter as ctk

ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue") 

dynList = [
    "Alice Smith",
    "Bob Jones",
    "Charlie Brown",
    "Diana Prince",
    "Evan Wright",
    "Fiona Gallagher"
]

def openUserInfo(userName):
    """Target function executed when a name button is clicked."""
    print(self=None) # allow only One
    print(f"Opening profile window for: {userName}")

class ContentCard(ctk.CTkFrame):
    """A light-themed card component where the name acts as a clickable button."""
    def __init__(self, master, name_string, click_callback):
        super().__init__(master, fg_color="#F2F2F2", corner_radius=8, border_width=1, border_color="#D1D1D1")
        
        self.avatar_lbl = ctk.CTkLabel(
            self, 
            text="👤", 
            font=("Arial", 18),
            fg_color="#E0E0E0", 
            text_color="#333333",
            width=35,
            height=35,
            corner_radius=6
        )
        self.avatar_lbl.pack(side="left", padx=(15, 5), pady=10)
        
        self.name_btn = ctk.CTkButton(
            self, 
            text=name_string, 
            font=("Arial", 14, "bold"),
            text_color="#1A1A1A",
            fg_color="transparent",
            hover_color="#E0E0E0",
            anchor="w",
            command=click_callback
        )
        self.name_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

class App(ctk.CTk):
    def __init__(self, data_source):
        super().__init__()
        self.title("Dynamic Name Directory")
        self.geometry("400x450")

        # scrollbar
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=15)

        #show list
        self.render_cards(data_source)

    def render_cards(self, name_list):
        for name in name_list:
            # asign name arg
            card = ContentCard(
                self.scroll_frame, 
                name_string=name,
                click_callback=lambda target_name=name: openUserInfo(target_name)
            )
            card.pack(fill="x", pady=5, padx=5)

if __name__ == "__main__":
    app = App(data_source=dynList)
    app.mainloop()
