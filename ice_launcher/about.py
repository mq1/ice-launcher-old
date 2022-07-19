# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from customtkinter import CTkFrame, CTkLabel
from ice_launcher.__about__ import __version__


class About(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.grid_columnconfigure(0, weight=1)

        self.app_name = CTkLabel(
            master=self,
            height=100,
            fg_color=("white", "gray38"),  # <- custom tuple-color
            text_font=("Roboto Medium", -20),  # font name and size in px
            text="ice-launcher",
        )
        self.app_name.grid(row=0, column=0, pady=20, padx=20, sticky="nswe")

        self.app_version = CTkLabel(master=self, text=__version__)
        self.app_version.grid(row=1, column=0, pady=20, padx=20)

        self.app_author = CTkLabel(master=self, text="Copyright © 2022 Manuel Quarneti")
        self.app_author.grid(row=2, column=0, pady=20, padx=20)

        self.app_license = CTkLabel(master=self, text="GPL-3.0 Licensed")
        self.app_license.grid(row=3, column=0, pady=20, padx=20)
