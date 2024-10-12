import glob
import os
import tkinter
from pathlib import Path
import customtkinter
from src.gui.CsvList import CsvList
from src.gui.NewMessage import NewMessage
from src.gui.Settings import Settings
from src.gui.Finder import Finder
from CTkMessagebox import CTkMessagebox

FOLDERPATH = Path(__file__).parent.parent.parent.resolve() / "src/resources/messages"


class HomePage(customtkinter.CTkFrame):
    def __init__(self, main_frame):

        self.main_frame = main_frame

        self.left_frame = customtkinter.CTkFrame(master=self.main_frame, width=350, corner_radius=0)
        self.left_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.right_frame = customtkinter.CTkFrame(master=self.main_frame, corner_radius=0)
        self.right_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)

        self.btn_new_message = customtkinter.CTkButton(master=self.left_frame, text="New Message", height=36,
                                                       corner_radius=8,
                                                       command=self.new_message)
        self.btn_new_message.pack(pady=(60, 10), padx=20, fill=tkinter.X)

        self.btn_find_leaker = customtkinter.CTkButton(master=self.left_frame, text="Find Leaker", height=36,
                                                       corner_radius=8,
                                                       command=self.find_leaker)
        self.btn_find_leaker.pack(pady=10, padx=20, fill=tkinter.X)

        self.btn_csv_generator = customtkinter.CTkButton(master=self.left_frame, text="People List", height=36,
                                                         corner_radius=8,
                                                         command=self.csv_list)
        self.btn_csv_generator.pack(pady=10, padx=20, fill=tkinter.X)

        self.btn_Settings = customtkinter.CTkButton(master=self.left_frame, text="Settings", height=36, corner_radius=8,
                                                    command=self.settings)
        self.btn_Settings.pack(side=tkinter.BOTTOM, pady=40, padx=20, fill=tkinter.X)

        self.recent_files_label = customtkinter.CTkLabel(master=self.right_frame, text="Recent Messages", corner_radius=8,
                                                         font=("Arial", 20))
        self.recent_files_label.pack(pady=(60, 0))
        self.recent_files = customtkinter.CTkScrollableFrame(master=self.right_frame, corner_radius=8,
                                                             height=540)
        self.recent_files.pack(pady=(10, 40), padx=20, fill=tkinter.X, expand=True)
        filelist = sorted(os.listdir(FOLDERPATH), key=lambda x: os.path.getmtime(FOLDERPATH / x), reverse=True)

        for file in filelist:
            self.file_frame = customtkinter.CTkFrame(master=self.recent_files, height=20)
            self.file_frame.pack(pady=(0, 10), padx=20, fill=tkinter.X)
            self.file_button = customtkinter.CTkButton(master=self.file_frame, text=file, corner_radius=8,
                                                       command=lambda filename=file: self.find_leaker(filename))
            self.file_button.pack(side=tkinter.LEFT, padx=(20, 10))
            self.bin_button = customtkinter.CTkButton(master=self.file_frame, text="delete", corner_radius=8, width=6,
                                                      command=lambda filename=file: self.delete_file(filename))
            self.bin_button.pack(side=tkinter.RIGHT, padx=(10, 20))

    def csv_list(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        CsvList(self.main_frame)


    def new_message(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        NewMessage(self.main_frame)


    def find_leaker(self, filename=None):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        Finder(self.main_frame, filename)


    def settings(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        Settings(self.main_frame)


    def delete_file(self, file):
        msg = CTkMessagebox(title="warning", message="do you want to delete " + file + "?", option_1="no",
                            option_2="yes")
        if msg.get() == "yes":
            try:
                os.remove(FOLDERPATH / file)
                for widget in self.recent_files.winfo_children():
                    if widget.winfo_children()[0].cget("text") == file:
                        widget.destroy()
            except Exception as e:
                CTkMessagebox(title="Error", message="error while deleting file", icon='warning', sound=True)


if __name__ == "__main__":
    root = customtkinter.CTk()
    root.geometry("960x540")
    root.title("Home Page")
    app = HomePage(root)

    root.mainloop()
