from customtkinter import CTkFrame, CTkLabel


class Settings(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.app_name = CTkLabel(
            master=self,
            height=100,
            fg_color=("white", "gray38"),  # <- custom tuple-color
            text_font=("Roboto Medium", -20),  # font name and size in px
            text="Settings",
        )
        self.app_name.pack(pady=20, padx=20, fill="x")
