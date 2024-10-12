import tkinter
import customtkinter
import os
from pathlib import Path
from CTkMessagebox import CTkMessagebox
from src.logic.FinderLogic import find

FOLDERPATH = Path(__file__).parent.parent.parent.resolve() / "src/resources/messages"


class Finder(customtkinter.CTkFrame):
    def __init__(self, main_frame, filename):

        self.main_frame = main_frame
        self.radvar = tkinter.IntVar()
        self.radvar.set(1)
        selected_file = tkinter.StringVar()
        selected_file.set("Select a file")
        if filename is not None:
            selected_file.set(filename)
            self.radvar.set(2)

        self.left_frame = customtkinter.CTkFrame(master=self.main_frame, width=350, corner_radius=8)
        self.left_frame.pack(side=tkinter.LEFT, fill=tkinter.X, padx=(60, 0))
        self.right_frame = customtkinter.CTkFrame(master=self.main_frame, corner_radius=8)
        self.right_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)
        self.backbutton = customtkinter.CTkButton(master=self.main_frame, text="←", corner_radius=8, height=30,
                                                  width=10, command=self.back_to)
        self.backbutton.place(x=20, y=10)


        self.optionlayout = customtkinter.CTkFrame(master=self.left_frame, corner_radius=8)
        self.optionlayout.pack(pady=60, padx=20, fill=tkinter.X)

        self.Title = customtkinter.CTkLabel(master=self.optionlayout, text="Search Options", corner_radius=8,
                                            font=("Arial", 20))
        self.Title.pack(pady=(10, 0))

        self.radio1 = customtkinter.CTkRadioButton(master=self.optionlayout,
                                                   text="Search in every watermarked text/email", variable=self.radvar,
                                                   value=1, command=self.toggle_text_file)
        self.radio1.pack(pady=(10, 10), padx=20, fill=tkinter.X)
        self.radio2 = customtkinter.CTkRadioButton(master=self.optionlayout,
                                                   text="Search in a specific watermarked text/email",
                                                   variable=self.radvar, value=2, command=self.toggle_text_file)
        self.radio2.pack(pady=(10, 10), padx=20, fill=tkinter.X)
        messages = os.listdir(FOLDERPATH)
        self.text_file = customtkinter.CTkOptionMenu(master=self.optionlayout,
                                                     variable=selected_file,
                                                     values=messages)
        self.text_file.pack(pady=(10, 10), padx=20, fill=tkinter.BOTH, expand=True)
        self.toggle_text_file()

        self.message_frame = customtkinter.CTkFrame(master=self.right_frame, corner_radius=8)
        self.message_frame.pack(pady=(60, 10), fill=tkinter.BOTH, expand=True)
        self.message_label = customtkinter.CTkLabel(master=self.message_frame, text="Message", corner_radius=8,
                                                    font=("Arial", 20))
        self.message_label.pack(pady=(10, 0))
        self.messagebox = customtkinter.CTkTextbox(master=self.message_frame, corner_radius=8)
        self.messagebox.pack(pady=(10, 10), padx=20, fill=tkinter.BOTH, expand=True)
        self.subit_button = customtkinter.CTkButton(master=self.message_frame, text="Submit", corner_radius=8,
                                                    height=30, command=lambda: self.search(selected_file))
        self.subit_button.pack(pady=(10, 20), padx=20, fill=tkinter.BOTH)

    def toggle_text_file(self):
        if self.radvar.get() == 2:
            self.text_file.configure(state="normal")
        else:
            self.text_file.configure(state="disabled")

    def back_to(self):
        from src.gui.HomePage import HomePage
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        HomePage(self.main_frame)

    def search(self, filename):
        text = self.messagebox.get("1.0", "end-1c")
        if self.radvar.get() == 1:
            Id, file = find(text)

        else:
            Id, file = find(text, FOLDERPATH / filename.get())

        if Id is not None:
            CTkMessagebox(title="Result", message="The person is: " + Id["mail"] + " \non:" + str(file))
        else:
            CTkMessagebox(title="Result", message="Person not found")


if __name__ == "__main__":
    # testa la classe
    root = customtkinter.CTk()
    root.geometry("960x540")
    root.title("Finder")
    app = Finder(root, None)
    root.mainloop()
