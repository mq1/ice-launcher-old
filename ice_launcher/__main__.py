# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import customtkinter
from customtkinter import CTk, CTkButton, CTkFrame
from ice_launcher.instances import Instances
from ice_launcher.news import News
from ice_launcher.settings import Settings
from ice_launcher.about import About
from ice_launcher.accounts import Accounts


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class App(CTk):
    WIDTH: int = 780
    HEIGHT: int = 520

    views: dict[str, CTkFrame]
    current_view: str = "instances"

    def __init__(self) -> None:
        super().__init__()

        self.views = {
            "instances": Instances(master=self),
            "news": News(master=self),
            "accounts": Accounts(master=self),
            "settings": Settings(master=self),
            "about": About(master=self),
        }

        self.title("Ice Launcher")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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

        # place all views in the same place
        for view in self.views.values():
            view.grid(row=0, column=1, pady=20, padx=20, sticky="nswe")

        self.update_main_frame()

    def on_closing(self, event=0) -> None:
        self.destroy()

    def update_main_frame(self) -> None:
        self.views[self.current_view].tkraise()
        self.__dict__[f"{self.current_view}_button"].configure(fg_color="#1F6AA5")

    def open_view(self, view: str) -> None:
        self.__dict__[f"{self.current_view}_button"].configure(fg_color=None)
        self.current_view = view
        self.update_main_frame()


if __name__ == "__main__":
    app: App = App()
    app.mainloop()
