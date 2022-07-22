# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from customtkinter import (
    CTkToplevel,
    CTkLabel,
    CTkComboBox,
    CTkEntry,
    CTkButton,
    StringVar,
)
from minecraft_launcher_lib.utils import get_available_versions, get_latest_version
from minecraft_launcher_lib.install import install_minecraft_version
from ice_launcher import dirs
from os import path


__instances_dir__: str = path.join(dirs.user_data_dir, "instances")


class NewInstance(CTkToplevel):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        self.title = "Add new instance"

        self.versions = get_available_versions(dirs.user_data_dir)
        self.version_ids = [version["id"] for version in self.versions]

        self.grid_columnconfigure(0, weight=1)

        self.app_name = CTkLabel(
            master=self,
            height=100,
            fg_color=("white", "gray38"),  # <- custom tuple-color
            text_font=("Roboto Medium", -20),  # font name and size in px
            text="New Instance",
        )
        self.app_name.grid(row=0, column=0, pady=20, padx=20, sticky="nswe")

        self.instance_name = CTkEntry(master=self, placeholder_text="My new instance")
        self.instance_name.grid(row=1, column=0, pady=10, padx=10, sticky="nswe")

        self.version = StringVar(value=get_latest_version()["release"])
        self.version_selector = CTkComboBox(
            master=self, values=self.version_ids, variable=self.version
        )
        self.version_selector.grid(row=2, column=0, pady=10, padx=10, sticky="nswe")

        self.create_button = CTkButton(
            master=self,
            text="Create",
            command=self.create_instance,
        )
        self.create_button.grid(row=3, column=0, pady=20, padx=20)

    def create_instance(self) -> None:
        print("Creating instance")
        dir = path.join(__instances_dir__, self.instance_name.get())
        install_minecraft_version(self.version.get(), dir)
        print("Done")
        self.destroy()
