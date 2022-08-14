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

from ice_launcher.components.heading import Heading
from ice_launcher.lib import ProgressCallbacks, instances, minecraft_versions

from .instances import Instances


class NewInstance(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.grid_columnconfigure(0, weight=1)

        heading = Heading(master=self, text="✨ Create a new instance")
        heading.grid(row=0, column=0, pady=20, padx=20, sticky="nwe")

        self.instance_name = CTkEntry(master=self, placeholder_text="My new instance")
        self.instance_name.grid(row=1, column=0, pady=10, padx=20, sticky="nswe")

        self.version = StringVar()
        self.version_selector = CTkComboBox(master=self, variable=self.version)
        self.version_selector.grid(row=2, column=0, pady=10, padx=20, sticky="nswe")

        # empty row as spacing
        self.grid_rowconfigure(3, weight=1)

        self.create_button = CTkButton(
            master=self,
            text="Create",
            command=self.create_instance,
        )
        self.create_button.grid(row=4, column=0, pady=(10, 20), padx=20, sticky="swe")

        Thread(target=self.update_versions).start()

    def update_versions(self) -> None:
        self.version_manifest = minecraft_versions.fetch_manifest()
        self.version_ids = [version.id for version in self.version_manifest.versions]
        self.version_selector.configure(values=self.version_ids)
        self.version.set(self.version_manifest.latest.release)

    def create_instance(self) -> None:
        instance_name = self.instance_name.get()
        version_id = self.version.get()

        for widget in self.winfo_children():
            widget.destroy()

        heading = Heading(master=self, text=f"🔄 Creating instance {instance_name}")
        heading.grid(row=0, column=0, pady=20, padx=20, sticky="nwe")

        self.grid_rowconfigure(1, weight=1)

        self.status_label = CTkLabel(
            master=self, text=f"Creating instance {instance_name}"
        )
        self.status_label.grid(row=2, column=0, pady=10, padx=20)

        self.progress_bar = CTkProgressBar(master=self)
        self.progress_bar.grid(row=3, column=0, pady=10, padx=20)

        self.grid_rowconfigure(4, weight=1)

        self.current_value = 0
        self.max_progress = 0

        def set_status(status: str) -> None:
            self.status_label.configure(text=status)

        def increment_value_by(value: int) -> None:
            self.current_value += value
            self.progress_bar.set(self.current_value / self.max_progress)

        def set_max(value: int) -> None:
            self.max_progress = value

        callbacks = ProgressCallbacks(
            set_max=set_max,
            increment_value_by=increment_value_by,
            set_status=set_status,
        )

        def new_instance():
            version = next(
                version
                for version in self.version_manifest.versions
                if version.id == version_id
            )

            instances.new(
                instance_name,
                version,
                callbacks,
            )
            self.master.open_page(None, Instances(master=self.master))  # type: ignore

        Thread(target=new_instance).start()
