import tkinter
import customtkinter
from pathlib import Path
from src.gui.HomePage import HomePage
from src.logic.Security import loginCheck
from CTkMessagebox import CTkMessagebox

ICONPATH = Path(__file__).parent.parent.resolve() / "gui/logo.ico"


class Login(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("960x600")
        self.title("Leaker Finder")
        self.iconbitmap(ICONPATH)

        customtkinter.set_default_color_theme("blue")

        self.main_frame = customtkinter.CTkFrame(self, corner_radius=8)
        self.main_frame.pack(fill=tkinter.BOTH, expand=True)

        self.login_frame = customtkinter.CTkFrame(master=self.main_frame, corner_radius=8)
        self.login_frame.pack(fill=tkinter.BOTH, expand=True, pady=50, padx=50)
        self.title_label = customtkinter.CTkLabel(master=self.login_frame, text="Leaker Finder", font=("Arial", 30),
                                                  corner_radius=8)
        self.title_label.pack(pady=20)
        self.login_label = customtkinter.CTkLabel(master=self.login_frame, text="Insert password:", corner_radius=8)
        self.login_label.pack(pady=(60, 10))

        self.password_box = customtkinter.CTkEntry(master=self.login_frame, show="*", corner_radius=8, height=30)
        self.password_box.pack(pady=(10, 10), padx=200, fill=tkinter.BOTH)

        self.login_button = customtkinter.CTkButton(master=self.login_frame, text="Login", corner_radius=8, height=30,
                                                    command=self.login)
        self.login_button.pack(pady=(10, 20), padx=200, fill=tkinter.BOTH)

    def login(self):
        correctpsw = loginCheck(self.password_box)
        if correctpsw:
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            HomePage(self.main_frame)
        else:
            CTkMessagebox(title="Wrong password", message="Wrong password",
                          icon="cancel", option_1="Ok", sound=True)


if __name__ == "__main__":
    app = Login()
    app.mainloop()
