# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import webbrowser
from threading import Thread
from tkinter import ttk

from customtkinter import CTkButton, CTkFrame, CTkLabel
from minecraft_launcher_lib.types import Article, Articles
from minecraft_launcher_lib.utils import get_minecraft_news

from ice_launcher.components.heading import Heading
from ice_launcher.components.scrollable_frame import ScrollableFrame


class News(CTkFrame):
    articles: Articles

    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.grid_columnconfigure(0, weight=1)

        heading = Heading(master=self, text="News")
        heading.grid(row=0, column=0, pady=20, padx=20, sticky="nwe")

        self.news_frame = ScrollableFrame(master=self)
        self.news_frame.grid(row=1, column=0, pady=20, padx=20, sticky="nswe")
        self.grid_rowconfigure(1, weight=1)

        Thread(target=self.update_news).start()

    def update_news(self) -> None:
        articles = get_minecraft_news()["article_grid"]

        for index, article in enumerate(articles):
            label = CTkLabel(
                master=self.news_frame.content,
                text=article["default_tile"]["title"],
                anchor="w",
            )
            label.grid(row=index * 2, column=0, pady=10, padx=0, sticky="nw")
            open_button = CTkButton(
                master=self.news_frame.content,
                text="Open",
                command=lambda: self.open_article(article),
            )
            open_button.grid(row=index * 2, column=1, pady=10, padx=(0, 10), sticky="e")
            separator = ttk.Separator(self.news_frame.content, orient="horizontal")
            separator.grid(
                row=index * 2 + 1,
                column=0,
                columnspan=2,
                pady=0,
                padx=(0, 10),
                sticky="ew",
            )

    def open_article(self, article: Article) -> None:
        url = f"https://www.minecraft.net{article['article_url']}"
        webbrowser.open(url)
