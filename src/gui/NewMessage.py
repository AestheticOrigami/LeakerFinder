import os
import tkinter
import customtkinter
from CTkToolTip import CTkToolTip
from pathlib import Path
from src.logic.WatermarkingAlgorithm import newLineWatermark, hiddenWatermark, contentBasedWatermark
from src.logic.MessagesManager import addFile, generateJson
from src.logic.EmailSender import sendEmail
from CTkMessagebox import CTkMessagebox

PEOPLELISTPATH = Path(__file__).parent.parent.resolve() / "resources/ListOfPeople"
MESSAGEJSONPATH = Path(__file__).parent.parent.resolve() / "resources/jsonMessages"
BANCHARACTERS = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|", "\n", "\t"]


class NewMessage(customtkinter.CTkFrame):
    def __init__(self, main_frame):

        self.main_frame = main_frame
        self.radio_var = customtkinter.IntVar()
        self.send_mail_var = customtkinter.IntVar()
        self.gen_json = customtkinter.IntVar()

        customtkinter.set_default_color_theme("blue")

        self.left_frame = customtkinter.CTkFrame(master=self.main_frame, corner_radius=0, width=100)
        self.left_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.right_frame = customtkinter.CTkFrame(master=self.main_frame, corner_radius=0)
        self.right_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)

        self.backbutton = customtkinter.CTkButton(master=self.left_frame, text="←", corner_radius=8, height=30,
                                                  width=10, command=self.backto)
        self.backbutton.place(x=20, y=10)

        self.csvfile = customtkinter.StringVar(value="group to send")
        self.textformat_var = customtkinter.StringVar(value="Mail")

        self.option_menu = customtkinter.CTkOptionMenu(master=self.left_frame, variable=self.textformat_var,
                                                       values=["Mail", "Testo"],
                                                       command=self.changeformat)
        self.option_menu.pack(pady=(60, 10), padx=20, fill=tkinter.X)

        self.csv_files = os.listdir(PEOPLELISTPATH)
        self.option_menu = customtkinter.CTkOptionMenu(master=self.left_frame, variable=self.csvfile,
                                                       values=self.csv_files)
        self.option_menu.pack(pady=(10, 10), padx=20, fill=tkinter.X)

        # selezione del tipo di watermarking

        self.Rad1 = customtkinter.CTkRadioButton(master=self.left_frame, text="Newline watermark", value=1,
                                                 variable=self.radio_var)
        self.Rad1.pack(pady=(60, 10), padx=20, fill=tkinter.X)
        self.Rad2 = customtkinter.CTkRadioButton(master=self.left_frame, text="Unicode hidden characters watermark󠅤",
                                                 value=2,
                                                 variable=self.radio_var)
        self.Rad2.pack(pady=10, padx=20, fill=tkinter.X)

        self.Rad3 = customtkinter.CTkRadioButton(master=self.left_frame, text="Syntactic-based watermark", value=3,
                                                 variable=self.radio_var)
        self.Rad3.pack(pady=10, padx=20, fill=tkinter.X)

        self.send_email = customtkinter.CTkCheckBox(master=self.left_frame, text="Invia Mail",
                                                    variable=self.send_mail_var)
        self.send_email.pack(pady=10, padx=20, fill=tkinter.X)

        self.json_save = customtkinter.CTkCheckBox(master=self.left_frame, text="Salva su json",
                                                   variable=self.gen_json)
        self.json_save.pack(pady=10, padx=20, fill=tkinter.X)

        self.csv_name_label = customtkinter.CTkLabel(master=self.left_frame, text="Nome del file json:",
                                                     corner_radius=8,
                                                     anchor="w")
        self.csv_name_label.pack(pady=10, padx=(20, 0), fill=tkinter.X)
        self.csv_name_entry = customtkinter.CTkEntry(master=self.left_frame, height=30)
        self.csv_name_entry.pack(pady=(0, 20), padx=20, fill=tkinter.X)

        self.genMailField()

        ttp_rad1 = CTkToolTip(self.Rad1,
                              "The watermark will insert a series of backspaces. Use the token '$$$' to specify where the backspaces should be placed within the text.",
                              wraplength=300)
        ttp_rad2 = CTkToolTip(self.Rad2,
                              "The watermark will insert a series of hidden characters. Append the token (*) to the end of a word where you want to hide these characters, otherwise the algorithm will peak a random word",
                              wraplength=300)
        ttp_rad3 = CTkToolTip(self.Rad3,
                              "The watermark will replace certain words with synonyms while preserving the meaning and context, using OpenAI and the model selected in 'settings'",
                              wraplength=300)

    def changeformat(self, val):

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        if val == "Mail":
            self.send_email.configure(state="normal")
            self.genMailField()
            self.gen_json.set(0)
            self.json_save.configure(state="normal")
        else:
            self.send_email.configure(state="disabled")
            self.genTextField()
            self.gen_json.set(1)
            self.json_save.configure(state="disabled")

    def genTextField(self):
        self.textbox = customtkinter.CTkTextbox(master=self.right_frame, corner_radius=8)

        self.textbox.pack(pady=(60, 20), padx=20, fill=tkinter.BOTH, expand=True)

        # submit button
        btn_submit = customtkinter.CTkButton(master=self.right_frame, text="Submit", height=36, corner_radius=8,
                                             command=self.Submit)
        btn_submit.pack(side=tkinter.BOTTOM, pady=(40, 20), padx=20, fill=tkinter.X)

    def genMailField(self):

        self.label_1 = customtkinter.CTkLabel(master=self.right_frame, text="Oggetto:", height=8, corner_radius=8,
                                              anchor="w")
        self.label_1.pack(pady=(68, 10), padx=20, fill=tkinter.X)

        self.object = customtkinter.CTkTextbox(master=self.right_frame, corner_radius=8, height=18)
        self.object.pack(pady=(10, 10), padx=20, fill=tkinter.X)

        self.label_2 = customtkinter.CTkLabel(master=self.right_frame, text="Testo:", height=8, corner_radius=8,
                                              anchor="w")
        self.label_2.pack(pady=(10, 10), padx=20, fill=tkinter.X)

        self.textbox = customtkinter.CTkTextbox(master=self.right_frame, corner_radius=8)
        self.textbox.pack(pady=(10, 20), padx=20, fill=tkinter.BOTH, expand=True)

        # submit button
        self.btn_submit = customtkinter.CTkButton(master=self.right_frame, text="Submit", height=36, corner_radius=8,
                                                  command=self.Submit)
        self.btn_submit.pack(side=tkinter.BOTTOM, pady=(40, 20), padx=20, fill=tkinter.X)

    def Submit(self):
        if self.radio_var.get() == 0:
            CTkMessagebox(title="Error", message="Seleziona un tipo di watermarking",
                          icon='warning', sound=False)
            return
        elif self.textformat_var.get() == "Mail" and self.object.get("0.0", "end-1c") == "":
            CTkMessagebox(title="Error", message="Inserisci un oggetto", icon='warning', sound=False)
            return
        elif self.textbox.get("0.0", "end-1c") == "":
            CTkMessagebox(title="Error", message="Inserisci un messaggio", icon='warning', sound=False)
        elif self.csvfile.get() == "group to send":
            CTkMessagebox(title="Error", message="Seleziona un gruppo", icon='warning', sound=False)
            return
        elif self.gen_json.get() == 1 and self.csv_name_entry.get() == "":
            for banchar in BANCHARACTERS:
                if banchar in self.csv_name_entry.get():
                    CTkMessagebox(title="Error", message="Carattere non valido nel nome del file", icon='warning',
                                  sound=True)
                    return
            CTkMessagebox(title="Error", message="Inserisci un nome per il file csv", icon='warning', sound=True)
            return

        watermarkedDict = {}

        if self.radio_var.get() == 1:
            watermarkedDict = newLineWatermark(self.textbox.get("0.0", "end-1c"), self.csvfile.get())
        elif self.radio_var.get() == 2:
            watermarkedDict = hiddenWatermark(self.textbox.get("0.0", "end-1c"), self.csvfile.get())
        elif self.radio_var.get() == 3:
            watermarkedDict = contentBasedWatermark(self.textbox.get("0.0", "end-1c"), self.csvfile.get())
        CTkMessagebox(title="Success", message="Messaggio creato correttamente", icon='check', sound=False)
        if self.textformat_var.get() == "Mail":
            obj = self.object.get("0.0", "end-1c")

        else:
            obj = self.csv_name_entry.get()

        addFile(obj, self.textbox.get("0.0", "end-1c"), watermarkedDict)
        if self.gen_json.get() == 1:
            generateJson(obj, watermarkedDict)
        if self.send_mail_var.get() == 1:
            sendEmail(watermarkedDict, self.object.get("0.0", "end-1c"))


    def backto(self):
        from src.gui.HomePage import HomePage
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.new_page = HomePage(self.main_frame)
