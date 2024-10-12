import tkinter
import customtkinter
from CTkMessagebox import CTkMessagebox
import src.logic.Security as Security

GPT_MODELS = ["gpt-4o-mini", "gpt-4o-mini-2024-07-18	", "gpt-4-turbo", "gpt-4-turbo-2024-04-09",
              "gpt-4-turbo-preview"]


class Settings(customtkinter.CTkFrame):
    def __init__(self, main_frame):
        super().__init__(main_frame)
        self.main_frame = main_frame

        self.left_frame = customtkinter.CTkFrame(master=self.main_frame, width=350, corner_radius=8)
        self.left_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=(60, 0),expand=True)
        self.right_frame = customtkinter.CTkFrame(master=self.main_frame, corner_radius=8)
        self.right_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)

        self.backbutton = customtkinter.CTkButton(master=self.main_frame, text="←", corner_radius=8, height=30,
                                                  width=10, command=self.back_to)
        self.backbutton.place(x=20, y=10)

        self.psw_frame = customtkinter.CTkFrame(master=self.left_frame, corner_radius=8)
        self.psw_frame.pack(pady=(60, 10), padx=(20, 0), fill=tkinter.X)

        self.password_title = customtkinter.CTkLabel(master=self.psw_frame, text="Password Reset", corner_radius=8,
                                                     font=("Arial", 20))
        self.password_title.pack(pady=(10, 0))

        self.password_label = customtkinter.CTkLabel(master=self.psw_frame, text="Current Password:",
                                                     corner_radius=8)
        self.password_label.pack(pady=(10, 0), padx=100, fill=tkinter.X)

        self.password_box = customtkinter.CTkEntry(master=self.psw_frame, show="*", corner_radius=8, height=30)
        self.password_box.pack(pady=(10, 10), padx=100, fill=tkinter.X)

        self.new_password_label = customtkinter.CTkLabel(master=self.psw_frame, text="New Password:",
                                                         corner_radius=8)
        self.new_password_label.pack(pady=(10, 0), padx=100, fill=tkinter.X)

        self.new_password_box = customtkinter.CTkEntry(master=self.psw_frame, show="*", corner_radius=8, height=30)
        self.new_password_box.pack(pady=(10, 10), padx=100, fill=tkinter.X)
        self.confirm_new_password_label = customtkinter.CTkLabel(master=self.psw_frame, text="Confirm New Password:",
                                                                 corner_radius=8)
        self.confirm_new_password_label.pack(pady=(10, 0), padx=100, fill=tkinter.X)

        self.confirm_new_password_box = customtkinter.CTkEntry(master=self.psw_frame, show="*", corner_radius=8,
                                                               height=30)
        self.confirm_new_password_box.pack(pady=(10, 10), padx=100, fill=tkinter.X)

        self.password_button = customtkinter.CTkButton(master=self.psw_frame, text="Change Password",
                                                       corner_radius=8,
                                                       height=30,
                                                       command=self.newpassword)
        self.password_button.pack(pady=(10, 20), padx=100, fill=tkinter.BOTH)

        self.credential_settings_frame = customtkinter.CTkFrame(master=self.right_frame, corner_radius=8)
        self.credential_settings_frame.pack(pady=(60, 10), padx=20)

        self.api_title = customtkinter.CTkLabel(master=self.credential_settings_frame, text="Credentials ",
                                                corner_radius=8,
                                                font=("Arial", 20))
        self.api_title.pack(pady=(10, 0))

        self.reset_mail_label = customtkinter.CTkLabel(master=self.credential_settings_frame,
                                                       text="change Mail Sender:",
                                                       corner_radius=8)
        self.reset_mail_label.pack(pady=(10, 0), padx=100, fill=tkinter.X)

        self.reset_mail_box = customtkinter.CTkTextbox(master=self.credential_settings_frame, corner_radius=8,
                                                       height=18)
        self.reset_mail_box.pack(pady=(0, 10), padx=100, fill=tkinter.X)

        self.reset_mail_button = customtkinter.CTkButton(master=self.credential_settings_frame, text="Apply",
                                                         corner_radius=8,
                                                         height=30, command=self.resetMail)
        self.reset_mail_button.pack(pady=(10, 10), padx=100, fill=tkinter.BOTH)

        self.reset_mail_password_label = customtkinter.CTkLabel(master=self.credential_settings_frame,
                                                                text="change Mail Sender password:", corner_radius=8)
        self.reset_mail_password_label.pack(pady=(10, 0), padx=100, fill=tkinter.X)

        self.reset_mai_password_box = customtkinter.CTkTextbox(master=self.credential_settings_frame, corner_radius=8,
                                                               height=18)
        self.reset_mai_password_box.pack(pady=(0, 10), padx=100, fill=tkinter.X)

        self.reset_mail_password_button = customtkinter.CTkButton(master=self.credential_settings_frame, text="Apply",
                                                                  corner_radius=8, height=30, command=self.resetPswMail)
        self.reset_mail_password_button.pack(pady=(10, 10), padx=100, fill=tkinter.BOTH)

        self.api_reset_chatgpt_label = customtkinter.CTkLabel(master=self.credential_settings_frame,
                                                              text="change ChatGpt key:",
                                                              corner_radius=8)
        self.api_reset_chatgpt_label.pack(pady=(10, 0), padx=100, fill=tkinter.X)

        self.api_reset_chatgpt_box = customtkinter.CTkTextbox(master=self.credential_settings_frame, corner_radius=8,
                                                              height=18)
        self.api_reset_chatgpt_box.pack(pady=(0, 10), padx=100, fill=tkinter.X)

        self.api_reset_chatgpt_button = customtkinter.CTkButton(master=self.credential_settings_frame, text="Apply",
                                                                corner_radius=8, height=30,
                                                                command=self.resetAPIChatGpt)
        self.api_reset_chatgpt_button.pack(pady=(10, 20), padx=100, fill=tkinter.BOTH)




        self.openai_stat_frame = customtkinter.CTkFrame(master=self.left_frame, corner_radius=8)
        self.openai_stat_frame.pack(pady=(10, 10), padx=(20, 0), fill=tkinter.X)
        self.openai_stat_title = customtkinter.CTkLabel(master=self.openai_stat_frame, text="OpenAI Statistics",
                                                        corner_radius=8,
                                                        font=("Arial", 20))
        self.openai_stat_title.pack(pady=(10, 0))

        self.openai_stat_token_used_label = customtkinter.CTkLabel(master=self.openai_stat_frame,
                                                                   text="Token used: " + str(
                                                                       Security.getinfo("tokenUsed")),
                                                                   corner_radius=8, height=30)
        self.openai_stat_token_used_label.pack(pady=(10, 10), padx=10, fill=tkinter.X)
        self.openai_stat_reset_button = customtkinter.CTkButton(master=self.openai_stat_frame, text="Reset Token",
                                                                corner_radius=8, height=30,
                                                                command=self.resetToken)
        self.openai_stat_reset_button.pack(pady=(10, 10), padx=10)

        self.chatgpt_models_title = customtkinter.CTkLabel(master=self.openai_stat_frame, text="ChatGPT Models:",
                                                           corner_radius=8,
                                                           )
        self.chatgpt_models_title.pack(pady=(0,20),padx=20)
        self.chatgpt_model_var = tkinter.StringVar()
        self.chatgpt_model_var.set(Security.getinfo("gptModel"))
        self.chatgp_models_list = customtkinter.CTkOptionMenu(master=self.openai_stat_frame, corner_radius=8,
                                                              height=18, variable=self.chatgpt_model_var,
                                                              values=GPT_MODELS, command=lambda var=self.chatgpt_model_var.get(): Security.changeGptModel(var))
        self.chatgp_models_list.pack(pady=(0,20),padx=20)
    def newpassword(self):
        if Security.loginCheck(self.password_box):
            if self.new_password_box.get() == self.confirm_new_password_box.get():
                if len(self.new_password_box.get()) < 8:
                    CTkMessagebox(title="Error", message="Password too short", sound=True)
                else:
                    if Security.changePassword(self.new_password_box.get()):
                        CTkMessagebox(title="Success", message="Password changed successfully",
                                      icon='check')
                        self.password_box.delete("0", "end")
                        self.new_password_box.delete("0", "end")
                        self.confirm_new_password_box.delete("0", "end")
                    else:
                        CTkMessagebox(title="Error", message="Error during password change", sound=True, icon='cancel')
            else:
                CTkMessagebox(title="Error", message="Passwords do not match", sound=True, icon='cancel')
        else:
            CTkMessagebox(title="Error", message="Wrong password", sound=True, icon='cancel')

    def resetAPIChatGpt(self):
        change = Security.changeAPIChatGpt(self.api_reset_chatgpt_box.get("1.0", "end-1c"))
        if change:
            CTkMessagebox(title="Success", message="Api Key changed successfully",
                          sound=True, icon='check')
        else:
            CTkMessagebox(title="Error", message="Api Key not changed", sound=True, icon='cancel')

        self.api_reset_chatgpt_box.delete("1.0", "end")

    def resetMail(self):
        change = Security.changeMail(self.reset_mail_box.get("1.0", "end-1c"))
        if change:
            CTkMessagebox(title="Success", message="Api Key changed successfully",
                          sound=True, icon='check')
        else:
            CTkMessagebox(title="Error", message="Api Key not changed", sound=True, icon='cancel')

        self.reset_mail_box.delete("1.0", "end")

    def resetPswMail(self):
        change = Security.changeMailPsw(self.reset_mai_password_box.get("1.0", "end-1c"))
        if change:
            CTkMessagebox(title="Success", message="Api Key changed successfully",
                          sound=True, icon='check')
        else:
            CTkMessagebox(title="Error", message="Api Key not changed", sound=True, icon='cancel')

        self.reset_mail_box.delete("1.0", "end")

    def back_to(self):
        from src.gui.HomePage import HomePage
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        HomePage(self.main_frame)

        return

    def resetToken(self):
        resp = CTkMessagebox(title="warning", message="Are you sure you want to reset the token?", icon='warning',
                             option_1="Yes", option_2="No")
        if resp.get() == "Yes":
            Security.resetToken()
            self.openai_stat_token_used_label.configure(text="Token used: " + str(Security.getinfo("tokenUsed")))
            CTkMessagebox(title="Success", message="Token reset successfully", sound=True, icon='check')


if __name__ == "__main__":
    root = customtkinter.CTk()
    root.title("Settings")
    root.geometry("960x600")
    settings = Settings(root)
    settings.pack(fill=tkinter.BOTH, expand=True)
    root.mainloop()
