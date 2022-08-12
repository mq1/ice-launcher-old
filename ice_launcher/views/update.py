# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import sys
import webbrowser

from customtkinter import CTkButton, CTkLabel, CTkToplevel

from ice_launcher import __version__


class Update(CTkToplevel):
    def __init__(self, master, latest_version: str) -> None:
        super().__init__(master=master)
        self.latest_version = latest_version
        self.title("Update")

        self.grid_columnconfigure(0, weight=1)

        self.current_release = CTkLabel(
            master=self, text=f"Current version: {__version__}"
        )
        self.current_release.grid(
            row=0, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="nswe"
        )

        self.latest_release = CTkLabel(
            master=self, text=f"Latest version: {latest_version}"
        )
        self.latest_release.grid(
            row=1, column=0, columnspan=2, pady=10, padx=20, sticky="nswe"
        )

        # empty row as spacing
        self.grid_rowconfigure(2, weight=1)

        self.update_question = CTkLabel(master=self, text="Do you want to update?")
        self.update_question.grid(row=3, column=0, columnspan=2, pady=(10, 20), padx=20)

        self.no_button = CTkButton(
            master=self, text="No", command=self.destroy, fg_color=None
        )
        self.no_button.grid(row=4, column=0, pady=10, padx=20)

        self.yes_button = CTkButton(
            master=self,
            text="Update",
            command=self.update,
        )
        self.yes_button.grid(row=4, column=1, pady=10, padx=20)

    def update(self) -> None:
        webbrowser.open(
            f"https://github.com/mq1/ice-launcher/releases/tag/{self.latest_version}"
        )
        sys.exit()
