# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from customtkinter import CTkButton, CTkFrame, CTkToplevel

from ice_launcher.components.heading import Heading
from ice_launcher.lib import instances


class EditInstance(CTkToplevel):
    def __init__(self, instance_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_name = instance_name
        self.title(instance_name)

        heading = Heading(master=self, text=instance_name)
        heading.grid(row=0, column=0, pady=20, padx=20, sticky="nwe")

        # empty row as spacing
        self.grid_rowconfigure(99, weight=1)

        button_bar = CTkFrame(master=self)
        button_bar.grid(row=100, column=0, pady=20, padx=20, sticky="swe")

        # empty column as spacing
        button_bar.grid_columnconfigure(0, weight=1)

        delete_button = CTkButton(
            master=button_bar,
            text="Delete",
            command=self.delete_instance,
        )
        delete_button.grid(row=0, column=1, pady=10, padx=10, sticky="nse")

    def delete_instance(self) -> None:
        instances.delete(self.instance_name)
        self.destroy()
