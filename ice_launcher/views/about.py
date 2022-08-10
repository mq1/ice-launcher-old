# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import tkinter
from importlib import resources
from os import path

from customtkinter import CTkFrame, CTkLabel
from PIL import Image, ImageTk

from ice_launcher.__about__ import __version__
from ice_launcher.components.heading import Heading


class About(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.grid_columnconfigure(0, weight=1)

        with resources.path("ice_launcher.assets", "ice-launcher.png") as image_path:
            self.logo_image = ImageTk.PhotoImage(
                Image.open(image_path).resize((100, 100))
            )
            logo = CTkLabel(master=self, image=self.logo_image)
            logo.grid(row=0, column=0, pady=(20, 0), sticky="nswe")

        app_name = CTkLabel(master=self, text="Ice Launcher", text_font=("Roboto Medium", 30))  # type: ignore
        app_name.grid(row=1, column=0, pady=10, padx=20, sticky="nwe")

        self.info_frame = CTkFrame(master=self)
        self.info_frame.grid(row=2, column=0, pady=20, padx=20, sticky="nswe")

        self.app_info = CTkLabel(
            master=self.info_frame,
            text=f"Version {__version__}\n\nCopyright © 2022-present Manuel Quarneti\n\nGPL-3.0 Licensed",
            justify=tkinter.LEFT,
        )
        self.app_info.grid(row=1, column=0, pady=20, padx=20, sticky="w")
