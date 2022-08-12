# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from subprocess import Popen
from tkinter import END, Text

from customtkinter import CTkFrame

from ice_launcher.components.heading import Heading


class Logs(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        self.grid_columnconfigure(0, weight=1)

        heading = Heading(master=self, text="🗒 Logs")
        heading.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="nwe")

        self.logs = Text(master=self, highlightthickness=0)
        self.logs.grid(row=1, column=0, pady=20, padx=20, sticky="nswe")
        self.grid_rowconfigure(1, weight=1)

    def update_logs(self, process: Popen):
        while process.poll() is None:
            output = process.stdout.readline()  # type: ignore
            self.logs.insert(END, output)
