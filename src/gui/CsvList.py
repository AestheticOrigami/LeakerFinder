import os
import tkinter
from pathlib import Path
import customtkinter
from CTkMessagebox import CTkMessagebox
from src.gui.CsvGen import CsvGen

PATHTOCSVFOLDER = Path(__file__).parent.parent.resolve() / "resources/ListOfPeople"


class CsvList(customtkinter.CTkFrame):

    def __init__(self, main_frame):

        self.main_frame = main_frame

        customtkinter.set_default_color_theme("blue")

        self.backbutton = customtkinter.CTkButton(master=self.main_frame, text="←", corner_radius=8, height=30,
                                                  width=10, command=self.backto)
        self.backbutton.place(x=20, y=10)

        self.plusbutton = customtkinter.CTkButton(master=self.main_frame, text="+", corner_radius=8, height=30,
                                                  width=20, command=self.addfile)
        self.plusbutton.place(relx=0.95, y=10)

        self.list_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.list_frame.pack(fill=tkinter.BOTH, expand=True, padx=60, pady=60)
        self.title = customtkinter.CTkLabel(master=self.list_frame, text="People List", font=("Arial", 20))
        self.title.pack(pady=(10, 10))
        self.scrollable_frame = customtkinter.CTkScrollableFrame(master=self.list_frame)
        self.scrollable_frame.pack(fill=tkinter.BOTH, expand=True, pady=20, padx=10)

        self.filelist = os.listdir(PATHTOCSVFOLDER)
        for file in self.filelist:
            self.file_frame = customtkinter.CTkFrame(master=self.scrollable_frame, height=40, corner_radius=8)
            self.file_frame.pack(fill=tkinter.BOTH, expand=True, pady=5)
            self.file_label = customtkinter.CTkLabel(master=self.file_frame, text=file)
            self.file_label.pack(fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)
            self.file_delete = customtkinter.CTkButton(master=self.file_frame, text="Delete", corner_radius=8,
                                                       height=30, width=10,
                                                       command=lambda filename=file: self.delete_file(filename))
            self.file_delete.pack(side=tkinter.RIGHT, padx=(20, 0))
            self.file_modify = customtkinter.CTkButton(master=self.file_frame, text="Modify", corner_radius=8,
                                                       height=30, width=10,
                                                       command=lambda filename=file: self.modifyfile(filename))
            self.file_modify.pack(side=tkinter.RIGHT, padx=(0, 10))

    def backto(self):
        from src.gui.HomePage import HomePage
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        HomePage(self.main_frame)

    def addfile(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        CsvGen(self.main_frame)

    def delete_file(self, file):
        resp = CTkMessagebox(title="warning", message="do you want to delete " + file + "?", option_1="no",
                             option_2="yes")
        if resp.get() == "yes":
            try:
                os.remove(PATHTOCSVFOLDER / file)
                for widget in self.scrollable_frame.winfo_children():
                    if widget.winfo_children()[0].cget("text") == file:
                        widget.destroy()
            except Exception as e:
                print(e)

    def modifyfile(self, file):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        CsvGen(self.main_frame, file)


def test():
    root = customtkinter.CTk()
    root.geometry("960x540")
    root.title("Finder")
    app = CsvList(root)
    app.pack(fill=tkinter.BOTH, expand=True)
    root.mainloop()


if __name__ == "__main__":
    test()
