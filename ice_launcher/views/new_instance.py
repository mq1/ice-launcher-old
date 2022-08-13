# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from threading import Thread

from customtkinter import (
    CTkButton,
    CTkComboBox,
    CTkEntry,
    CTkFrame,
    CTkLabel,
    CTkProgressBar,
    StringVar,
)
from minecraft_launcher_lib.types import CallbackDict

from ice_launcher.lib import instances, minecraft_versions


class NewInstance(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

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
        version_manifest = minecraft_versions.fetch_manifest()
        self.version_ids = [version.id for version in version_manifest.versions]
        self.version_selector.configure(values=self.version_ids)
        self.version.set(version_manifest.latest.release)

    def create_instance(self) -> None:
        instance_name = self.instance_name.get()
        version_id = self.version.get()

        for widget in self.winfo_children():
            widget.destroy()

        self.status_label = CTkLabel(master=self, text="Creating instance...")
        self.status_label.grid(row=0, column=0, pady=10, padx=20)

        self.progress_bar = CTkProgressBar(master=self)
        self.progress_bar.grid(row=1, column=0, pady=10, padx=20)
        self.max_progress = 0

        def set_status(status: str) -> None:
            self.status_label.configure(text=status)

        def set_progress(progress: int) -> None:
            self.progress_bar.set(progress / self.max_progress)

        def set_max(value: int) -> None:
            self.max_progress = value

        callback: CallbackDict = {
            "setStatus": set_status,
            "setProgress": set_progress,
            "setMax": set_max,
        }

        def new_instance():
            instances.new(
                instance_name,
                version_id,
                callback,
            )
            self.master.open_view("instances")  # type: ignore

        Thread(target=new_instance).start()
