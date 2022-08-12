# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from importlib import resources
from threading import Thread
from tkinter import PhotoImage

import customtkinter
from customtkinter import CTk, CTkButton, CTkFrame

from ice_launcher.lib import config, updater
from ice_launcher.views.about import About
from ice_launcher.views.accounts import Accounts
from ice_launcher.views.instances import Instances
from ice_launcher.views.news import News
from ice_launcher.views.settings import Settings
from ice_launcher.views.update import Update

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(CTk):
    WIDTH: int = 780
    HEIGHT: int = 520
    current_view: str = "instances"

    def __init__(self) -> None:
        super().__init__()

        self.title("Ice Launcher")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # set app icon
        with resources.path("ice_launcher.assets", "ice-launcher.png") as image_path:
            self.app_icon = PhotoImage(file=image_path)
            self.wm_iconphoto(True, self.app_icon)

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navigator = CTkFrame(master=self, width=180, corner_radius=0)  # type: ignore
        self.navigator.grid(row=0, column=0, sticky="nswe")

        self.instances_button = CTkButton(
            master=self.navigator,
            text="Instances",
            command=lambda: self.open_view("instances"),
            border_width=2,
            fg_color=None,
        )
        self.instances_button.grid(
            row=0, column=0, pady=(20, 10), padx=20, sticky="nswe"
        )

        self.news_button = CTkButton(
            master=self.navigator,
            text="News",
            command=lambda: self.open_view("news"),
            border_width=2,
            fg_color=None,
        )
        self.news_button.grid(row=1, column=0, pady=10, padx=20)

        self.accounts_button = CTkButton(
            master=self.navigator,
            text="Accounts",
            command=lambda: self.open_view("accounts"),
            border_width=2,
            fg_color=None,
        )
        self.accounts_button.grid(row=2, column=0, pady=10, padx=20)

        self.settings_button = CTkButton(
            master=self.navigator,
            text="Settings",
            command=lambda: self.open_view("settings"),
            border_width=2,
            fg_color=None,
        )
        self.settings_button.grid(row=3, column=0, pady=10, padx=20)

        # empty row as spacing
        self.navigator.grid_rowconfigure(4, weight=1)

        self.about_button = CTkButton(
            master=self.navigator,
            text="About",
            command=lambda: self.open_view("about"),
            border_width=2,
            fg_color=None,
        )
        self.about_button.grid(row=5, column=0, pady=(10, 20), padx=20)

        self.view = CTkFrame(master=self)
        self.open_view("instances")

        if config.read()["automatically_check_for_updates"]:
            Thread(target=self.check_for_updates).start()

    def on_closing(self, event=0) -> None:
        self.destroy()

    def update_main_frame(self) -> None:
        for widget in self.view.winfo_children():
            widget.destroy()

        match self.current_view:
            case "instances":
                self.view = Instances(master=self)
            case "news":
                self.view = News(master=self)
            case "accounts":
                self.view = Accounts(master=self)
            case "settings":
                self.view = Settings(master=self)
            case "about":
                self.view = About(master=self)

        self.view.grid(row=0, column=1, pady=20, padx=20, sticky="nswe")

        self.__dict__[f"{self.current_view}_button"].configure(fg_color="#1F6AA5")

    def open_view(self, view: str) -> None:
        self.__dict__[f"{self.current_view}_button"].configure(fg_color=None)
        self.current_view = view
        self.update_main_frame()

    def check_for_updates(self) -> None:
        latest_version = updater.check_for_updates()
        if latest_version:
            Update(master=self, latest_version=latest_version)


def main():
    App().mainloop()


if __name__ == "__main__":
    main()
