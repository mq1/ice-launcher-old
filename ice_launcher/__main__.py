# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from importlib import resources
from threading import Thread
from tkinter import PhotoImage
from typing import Optional

from customtkinter import (
    CTk,
    CTkButton,
    CTkFrame,
    set_appearance_mode,
    set_default_color_theme,
)

from ice_launcher.lib import launcher_config, launcher_updater
from ice_launcher.views import About, Accounts, Instances, Logs, News, Settings, Update

set_appearance_mode("dark")
set_default_color_theme("blue")


class App(CTk):
    current_active_button: Optional[CTkButton] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Ice Launcher")
        self.geometry("780x520")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # set app icon
        with resources.path("ice_launcher.assets", "ice-launcher.png") as image_path:
            self.app_icon = PhotoImage(file=image_path)
            self.wm_iconphoto(True, self.app_icon)

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        navigator = CTkFrame(master=self, width=180, corner_radius=0)  # type: ignore
        navigator.grid(row=0, column=0, sticky="nswe")

        instances_button = CTkButton(
            master=navigator,
            text="Instances",
            command=lambda: self.open_page(instances_button, Instances(master=self)),
            border_width=2,
            fg_color=None,
        )
        instances_button.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="nswe")

        news_button = CTkButton(
            master=navigator,
            text="News",
            command=lambda: self.open_page(news_button, News(master=self)),
            border_width=2,
            fg_color=None,
        )
        news_button.grid(row=1, column=0, pady=10, padx=20)

        accounts_button = CTkButton(
            master=navigator,
            text="Accounts",
            command=lambda: self.open_page(accounts_button, Accounts(master=self)),
            border_width=2,
            fg_color=None,
        )
        accounts_button.grid(row=2, column=0, pady=10, padx=20)

        settings_button = CTkButton(
            master=navigator,
            text="Settings",
            command=lambda: self.open_page(settings_button, Settings(master=self)),
            border_width=2,
            fg_color=None,
        )
        settings_button.grid(row=3, column=0, pady=10, padx=20)

        # empty row as spacing
        navigator.grid_rowconfigure(50, weight=1)

        logs_button = CTkButton(
            master=navigator,
            text="Logs",
            command=lambda: self.open_page(logs_button, Logs(master=self)),
            border_width=2,
            fg_color=None,
        )
        logs_button.grid(row=100, column=0, pady=10, padx=20)

        about_button = CTkButton(
            master=navigator,
            text="About",
            command=lambda: self.open_page(about_button, About(master=self)),
            border_width=2,
            fg_color=None,
        )
        about_button.grid(row=101, column=0, pady=(10, 20), padx=20)

        self.current_page = CTkFrame(master=self)
        self.open_page(instances_button, Instances(master=self))

        if launcher_config.read().automatically_check_for_updates:
            Thread(target=self.check_for_updates).start()

    def on_closing(self, event=0) -> None:
        self.destroy()

    def open_page(self, button: Optional[CTkButton], page: CTkFrame) -> None:
        if self.current_active_button:
            self.current_active_button.configure(fg_color=None)

        if button:
            self.current_active_button = button
            self.current_active_button.configure(fg_color="#1F6AA5")

        for widget in self.current_page.winfo_children():
            widget.destroy()
        self.current_page.destroy()

        self.current_page = page
        self.current_page.grid(row=0, column=1, pady=20, padx=20, sticky="nswe")

    def check_for_updates(self) -> None:
        latest_version = launcher_updater.check_for_updates()
        if latest_version:
            Update(master=self, latest_version=latest_version)


def main():
    App().mainloop()


if __name__ == "__main__":
    main()
