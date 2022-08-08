# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from customtkinter import (
    BooleanVar,
    CTkButton,
    CTkEntry,
    CTkFrame,
    CTkLabel,
    CTkSwitch,
    StringVar,
)

from .lib import config


class Settings(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.app_config = config.read()

        self.grid_columnconfigure(0, weight=1)

        self.title_frame = CTkFrame(master=self, fg_color="gray38")
        self.title_frame.grid(row=0, column=0, pady=20, padx=20, sticky="nswe")

        self.view_name = CTkLabel(
            master=self.title_frame,
            text_font=("Roboto Medium", 30),
            text="Settings",
        )
        self.view_name.grid(row=0, column=0, pady=20, padx=20, sticky="nswe")

        self.automatically_check_for_updates = BooleanVar()
        automatically_check_for_updates_frame = CTkFrame(master=self)
        automatically_check_for_updates_frame.grid(
            row=1, column=0, pady=5, padx=20, sticky="we"
        )
        automatically_check_for_updates_label = CTkLabel(
            master=automatically_check_for_updates_frame,
            text="Automatically check for updates",
            anchor="w",
        )
        automatically_check_for_updates_label.grid(
            row=0, column=0, pady=10, padx=20, sticky="w"
        )
        automatically_check_for_updates_frame.grid_columnconfigure(0, weight=1)
        automatically_check_for_updates_switch = CTkSwitch(
            master=automatically_check_for_updates_frame,
            variable=self.automatically_check_for_updates,
            text="",
        )
        automatically_check_for_updates_switch.grid(
            row=0, column=1, pady=10, padx=20, sticky="e"
        )

        self.jvm_options = StringVar()
        jvm_options_frame = CTkFrame(master=self)
        jvm_options_frame.grid(row=2, column=0, pady=5, padx=20, sticky="we")
        jvm_options_label = CTkLabel(
            master=jvm_options_frame, text="JVM options", anchor="w"
        )
        jvm_options_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        jvm_options_frame.grid_columnconfigure(0, weight=1)
        jvm_options_entry = CTkEntry(
            master=jvm_options_frame, textvariable=self.jvm_options
        )
        jvm_options_entry.grid(row=0, column=1, pady=10, padx=20, sticky="e")

        self.jvm_memory = StringVar()
        jvm_memory_frame = CTkFrame(master=self)
        jvm_memory_frame.grid(row=3, column=0, pady=5, padx=20, sticky="we")
        jvm_memory_label = CTkLabel(
            master=jvm_memory_frame, text="JVM memory", anchor="w"
        )
        jvm_memory_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        jvm_memory_frame.grid_columnconfigure(0, weight=1)
        jvm_memory_entry = CTkEntry(
            master=jvm_memory_frame, textvariable=self.jvm_memory
        )
        jvm_memory_entry.grid(row=0, column=1, pady=10, padx=20, sticky="e")

        # empty row as spacing
        self.grid_rowconfigure(99, weight=1)

        self.button_bar = CTkFrame(master=self)
        self.button_bar.grid(row=100, column=0, pady=0, padx=0, sticky="swe")

        # empty column as spacing
        self.button_bar.grid_columnconfigure(0, weight=1)

        self.reset_button = CTkButton(
            master=self.button_bar,
            text="Reset to default settings",
            command=self.reset_to_default_settings,
        )
        self.reset_button.grid(row=0, column=1, pady=10, padx=10, sticky="se")

        self.save_button = CTkButton(
            master=self.button_bar,
            text="Save",
            command=self.save,
        )
        self.save_button.grid(row=0, column=2, pady=10, padx=10, sticky="se")

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
