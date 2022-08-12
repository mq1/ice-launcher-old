# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import tkinter
import webbrowser
from importlib import resources
from tkinter import PhotoImage

from customtkinter import CTkButton, CTkFrame, CTkLabel

from ice_launcher import __version__


class About(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.grid_columnconfigure(0, weight=1)

        with resources.path("ice_launcher.assets", "ice-launcher.png") as image_path:
            self.logo_image = PhotoImage(file=image_path).subsample(5)
            logo = CTkLabel(master=self, image=self.logo_image)
            logo.grid(row=0, column=0, pady=(20, 0), sticky="nswe")

        app_name = CTkLabel(master=self, text="Ice Launcher", text_font=("Roboto Medium", 30))  # type: ignore
        app_name.grid(row=1, column=0, pady=10, padx=20, sticky="nwe")

        self.info_frame = CTkFrame(master=self)
        self.info_frame.grid(row=2, column=0, pady=20, padx=20, sticky="nswe")

        self.app_info = CTkLabel(
            master=self.info_frame,
            text=f"Version {__version__}\n\nCopyright © 2022-present Manuel Quarneti",
            justify=tkinter.LEFT,
        )
        self.app_info.grid(row=1, column=0, pady=20, padx=20, sticky="w")

        # empty row as spacing
        self.grid_rowconfigure(99, weight=1)

        links_bar = CTkFrame(master=self)
        links_bar.grid(row=100, column=0, pady=0, padx=0, sticky="swe")

        # empty column as spacing
        links_bar.grid_columnconfigure(0, weight=1)

        license_button = CTkButton(
            master=links_bar,
            text="GPL-3.0 Licensed ↗️",
            command=lambda: webbrowser.open(
                "https://github.com/mq1/ice-launcher/blob/main/LICENSE.txt"
            ),
        )
        license_button.grid(row=0, column=1, pady=10, padx=10)

        source_code_button = CTkButton(
            master=links_bar,
            text="Source Code ↗️",
            command=lambda: webbrowser.open("https://github.com/mq1/ice-launcher"),
        )
        source_code_button.grid(row=0, column=2, pady=10, padx=10, sticky="nse")
