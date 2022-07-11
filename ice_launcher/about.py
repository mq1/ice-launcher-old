from customtkinter import CTkFrame, CTkLabel
from ice_launcher import __version__


class About(CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)

        self.app_name = CTkLabel(
            master=self,
            height=100,
            fg_color=("white", "gray38"),  # <- custom tuple-color
            text_font=("Roboto Medium", -20),  # font name and size in px
            text="ice-launcher",
        )
        self.app_name.pack(pady=20, padx=20, fill="x")

        self.app_version = CTkLabel(master=self, text=__version__)
        self.app_version.pack(pady=10, padx=20, fill="x")

        self.app_author = CTkLabel(master=self, text="Copyright © 2022 Manuel Quarneti")
        self.app_author.pack(pady=(10, 20), padx=20, fill="x")

        self.app_license = CTkLabel(master=self, text="GPL-3.0 Licensed")
        self.app_license.pack(pady=(10, 20), padx=20, fill="x")
