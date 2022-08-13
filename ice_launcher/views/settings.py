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
from ice_launcher.lib import launcher_config


class Settings(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)
        self.grid_columnconfigure(0, weight=1)

        heading = Heading(master=self, text="⚙️ Settings")
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

        self.jvm_arguments = StringVar()
        jvm_arguments_label = CTkLabel(
            master=settings_frame.content, text="JVM arguments", anchor="w"
        )
        jvm_arguments_label.grid(row=2, column=0, pady=10, padx=0, sticky="w")
        jvm_arguments_entry = CTkEntry(
            master=settings_frame.content, textvariable=self.jvm_arguments
        )
        jvm_arguments_entry.grid(row=2, column=1, pady=10, padx=(0, 10), sticky="e")

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
            text="Reset to default settings ♻️",
            fg_color=None,
            border_width=2,
            command=self.reset_to_default_settings,
        )
        self.reset_button.grid(row=0, column=1, pady=10, padx=10, sticky="nse")

        self.save_button = CTkButton(
            master=self.button_bar,
            text="Save ✅",
            command=self.save,
        )
        self.save_button.grid(row=0, column=2, pady=10, padx=10, sticky="nse")

        self.update_settings(launcher_config.read())

    def update_settings(self, config: launcher_config.Config) -> None:
        self.automatically_check_for_updates.set(config.automatically_check_for_updates)
        self.jvm_arguments.set(" ".join(config.jvm_arguments))
        self.jvm_memory.set(config.jvm_memory)

    def reset_to_default_settings(self) -> None:
        default_config = launcher_config.Config()
        self.update_settings(default_config)

    def save(self) -> None:
        config = launcher_config.read()

        config.automatically_check_for_updates = (
            self.automatically_check_for_updates.get()
        )
        config.jvm_arguments = self.jvm_arguments.get().split()
        config.jvm_memory = self.jvm_memory.get()

        launcher_config.write(config)
