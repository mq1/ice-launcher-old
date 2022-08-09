# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from threading import Thread

from customtkinter import CTkButton, CTkComboBox, CTkEntry, CTkToplevel, StringVar
from minecraft_launcher_lib.utils import get_latest_version

from ice_launcher.lib import instances, versions


class NewInstance(CTkToplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Add new instance")
        self.geometry("250x200")

        self.grid_columnconfigure(0, weight=1)

        self.instance_name = CTkEntry(master=self, placeholder_text="My new instance")
        self.instance_name.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="nswe")

        self.version = StringVar()
        self.version_selector = CTkComboBox(master=self, variable=self.version)
        self.version_selector.grid(row=1, column=0, pady=10, padx=20, sticky="nswe")

        # empty row as spacing
        self.grid_rowconfigure(2, weight=1)

        self.create_button = CTkButton(
            master=self,
            text="Create",
            command=self.create_instance,
        )
        self.create_button.grid(row=3, column=0, pady=(10, 20), padx=20)

        Thread(target=self.update_versions).start()

    def update_versions(self) -> None:
        av = versions.get_available()
        self.version_ids = [version["id"] for version in av]
        self.version_selector.configure(values=self.version_ids)
        self.version.set(get_latest_version()["release"])

    def create_instance(self) -> None:
        instances.new(self.instance_name.get(), self.version.get())
        self.destroy()
