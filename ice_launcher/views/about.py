# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import tkinter

from customtkinter import CTkFrame, CTkLabel

from ice_launcher.__about__ import __version__
from ice_launcher.components.heading import Heading


class About(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.grid_columnconfigure(0, weight=1)

        heading = Heading(master=self, text="Ice Launcher")
        heading.grid(row=0, column=0, pady=20, padx=20, sticky="nwe")

        self.info_frame = CTkFrame(master=self)
        self.info_frame.grid(row=1, column=0, pady=20, padx=20, sticky="nswe")
        self.info_frame.grid_columnconfigure(1, weight=1)

        self.app_info = CTkLabel(
            master=self.info_frame,
            text=f"Version {__version__}\n\nCopyright © 2022-present Manuel Quarneti\n\nGPL-3.0 Licensed",
            justify=tkinter.LEFT,
        )
        self.app_info.grid(row=1, column=0, pady=20, padx=20, sticky="w")
