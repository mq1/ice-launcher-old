# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from customtkinter import BooleanVar, CTkButton, CTkFrame, CTkLabel, CTkSwitch

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

        self.automatically_check_for_updates_switch = CTkSwitch(
            master=self,
            text="Automatically check for updates",
            variable=self.automatically_check_for_updates,
        )
        self.automatically_check_for_updates_switch.grid(
            row=1, column=0, pady=10, padx=20, sticky="w"
        )

        # empty row as spacing
        self.grid_rowconfigure(2, weight=1)

        self.button_bar = CTkFrame(master=self)
        self.button_bar.grid(row=3, column=0, pady=0, padx=0, sticky="nswe")

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

    def reset_to_default_settings(self) -> None:
        self.app_config = config.default()
        self.update_settings()

    def save(self) -> None:
        self.app_config[
            "automatically_check_for_updates"
        ] = self.automatically_check_for_updates.get()

        config.write(self.app_config)
