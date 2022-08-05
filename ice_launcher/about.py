# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import tkinter
from importlib.metadata import version

from customtkinter import CTkFrame, CTkLabel


class About(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.grid_columnconfigure(0, weight=1)

        self.title_frame = CTkFrame(master=self, fg_color="gray38")
        self.title_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nswe")

        self.app_name = CTkLabel(
            master=self.title_frame,
            text_font=("Roboto Medium", 30),
            text="Ice Launcher",
        )
        self.app_name.grid(row=0, column=0, pady=20, padx=20, sticky="nswe")

        self.info_frame = CTkFrame(master=self)
        self.info_frame.grid(row=1, column=0, pady=20, padx=20, sticky="nswe")
        self.info_frame.grid_columnconfigure(1, weight=1)

        self.app_info = CTkLabel(
            master=self.info_frame,
            text=f"Version {version('ice-launcher')}\n\nCopyright © 2022-present Manuel Quarneti\n\nGPL-3.0 Licensed",
            justify=tkinter.LEFT,
        )
        self.app_info.grid(row=1, column=0, pady=20, padx=20, sticky="w")
