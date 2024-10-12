import os
import tkinter
from pathlib import Path
from src.logic.MessagesManager import generateCsv
import customtkinter
from CTkMessagebox import CTkMessagebox

PATHTOCSVFOLDER = Path(__file__).parent.parent.resolve() / "resources/ListOfPeople"


class CsvGen(customtkinter.CTkFrame):
    BANCHARACTERS = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|", "\n", "\t"]

    def __init__(self, main_frame, file=None):
        self.main_frame = main_frame

        customtkinter.set_default_color_theme("blue")

        self.main_frame = customtkinter.CTkFrame(self.main_frame)
        self.main_frame.pack(fill=tkinter.BOTH, expand=True)

        self.backbutton = customtkinter.CTkButton(master=self.main_frame, text="←", corner_radius=8, height=30,
                                                  width=10, command=self.backto)
        self.backbutton.place(x=20, y=10)

        self.label_textbox = customtkinter.CTkLabel(master=self.main_frame, text="Name of the file:", corner_radius=8,
                                                    anchor="w")
        self.label_textbox.pack(pady=(60, 10), padx=20, fill=tkinter.X)
        self.textbox = customtkinter.CTkTextbox(master=self.main_frame, corner_radius=8, height=20, )
        self.textbox.pack(pady=(0, 10), padx=20, fill=tkinter.BOTH)

        self.label_csvbox = customtkinter.CTkLabel(master=self.main_frame, text="List of mail:", corner_radius=8,
                                                   anchor="w")
        self.label_csvbox.pack(pady=0, padx=20, fill=tkinter.X)
        self.csvbox = customtkinter.CTkTextbox(master=self.main_frame, corner_radius=8)
        self.csvbox.pack( padx=20,fill=tkinter.BOTH, expand=True)

        self.Button = customtkinter.CTkButton(master=self.main_frame, text="Generate", corner_radius=8, height=30,
                                              command=lambda: self.generate(self.csvbox, self.textbox))
        self.Button.pack(pady=(10, 20), padx=20, fill=tkinter.BOTH)

        if file is not None:
            filepath = PATHTOCSVFOLDER / file
            with open(filepath, "r") as f:
                data = f.read()
                self.csvbox.insert("1.0", data)
            self.textbox.insert("1.0", file)

    def generate(self, textbox, name):
        text = textbox.get("1.0", "end-1c")
        filename = name.get("1.0", "end-1c")

        banned = False
        for char in self.BANCHARACTERS:
            if char in filename:
                banned = True
                break

        if banned:
            CTkMessagebox(title="Error", message="Invalid character inside the name", icon='warning',
                          sound=True)
        elif filename == "" or filename == "\n" or filename == "\t":
            CTkMessagebox(title="Error", message="Insert a name", icon='warning', sound=True)
        elif text == "":
            CTkMessagebox(title="Error", message="Insert a mail", icon='warning', sound=True)
        else:
            generateCsv(text, filename)

    def backto(self):

        from src.gui.CsvList import CsvList
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        CsvList(self.main_frame)

