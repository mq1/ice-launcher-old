# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from tkinter import ttk

from customtkinter import (
    BooleanVar,
    CTkButton,
    CTkEntry,
    CTkFrame,
    CTkLabel,
    CTkSwitch,
    StringVar,
)

from ice_launcher.components.heading import Heading
from ice_launcher.components.scrollable_frame import ScrollableFrame
from ice_launcher.lib import config


class Settings(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.app_config = config.read()

        self.grid_columnconfigure(0, weight=1)

        heading = Heading(master=self, text="Settings")
        heading.grid(row=0, column=0, pady=20, padx=20, sticky="nwe")

        settings_frame = ScrollableFrame(master=self)
        settings_frame.grid(row=1, column=0, pady=20, padx=20, sticky="nswe")
        self.grid_rowconfigure(1, weight=1)

        self.automatically_check_for_updates = BooleanVar()
        automatically_check_for_updates_label = CTkLabel(
            master=settings_frame.content,
            text="Automatically check for updates",
            anchor="w",
        )
        automatically_check_for_updates_label.grid(
            row=0, column=0, pady=10, padx=0, sticky="w"
        )
        automatically_check_for_updates_switch = CTkSwitch(
            master=settings_frame.content,
            variable=self.automatically_check_for_updates,
            text="",
        )
        automatically_check_for_updates_switch.grid(
            row=0, column=1, pady=10, padx=(0, 10), sticky="e"
        )

        separator = ttk.Separator(settings_frame.content, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=2, pady=0, padx=(0, 10), sticky="ew")

        self.jvm_options = StringVar()
        jvm_options_label = CTkLabel(
            master=settings_frame.content, text="JVM options", anchor="w"
        )
        jvm_options_label.grid(row=2, column=0, pady=10, padx=0, sticky="w")
        jvm_options_entry = CTkEntry(
            master=settings_frame.content, textvariable=self.jvm_options
        )
        jvm_options_entry.grid(row=2, column=1, pady=10, padx=(0, 10), sticky="e")

        separator = ttk.Separator(settings_frame.content, orient="horizontal")
        separator.grid(row=3, column=0, columnspan=2, pady=0, padx=(0, 10), sticky="ew")

        self.jvm_memory = StringVar()
        jvm_memory_label = CTkLabel(
            master=settings_frame.content, text="JVM memory", anchor="w"
        )
        jvm_memory_label.grid(row=4, column=0, pady=10, padx=0, sticky="w")
        jvm_memory_entry = CTkEntry(
            master=settings_frame.content, textvariable=self.jvm_memory
        )
        jvm_memory_entry.grid(row=4, column=1, pady=10, padx=(0, 10), sticky="e")

        self.button_bar = CTkFrame(master=self)
        self.button_bar.grid(row=100, column=0, pady=0, padx=0, sticky="swe")

        # empty column as spacing
        self.button_bar.grid_columnconfigure(0, weight=1)

        self.reset_button = CTkButton(
            master=self.button_bar,
            text="Reset to default settings",
            command=self.reset_to_default_settings,
        )
        self.reset_button.grid(row=0, column=1, pady=10, padx=10, sticky="nse")

        self.save_button = CTkButton(
            master=self.button_bar,
            text="Save",
            command=self.save,
        )
        self.save_button.grid(row=0, column=2, pady=10, padx=10, sticky="nse")

        self.update_settings()

    def update_settings(self) -> None:
        self.automatically_check_for_updates.set(
            self.app_config["automatically_check_for_updates"]
        )
        self.jvm_options.set(" ".join(self.app_config["jvm_options"]))
        self.jvm_memory.set(self.app_config["jvm_memory"])

    def reset_to_default_settings(self) -> None:
        self.app_config = config.default()
        self.update_settings()

    def save(self) -> None:
        self.app_config[
            "automatically_check_for_updates"
        ] = self.automatically_check_for_updates.get()
        self.app_config["jvm_options"] = self.jvm_options.get().split()
        self.app_config["jvm_memory"] = self.jvm_memory.get()

        config.write(self.app_config)
