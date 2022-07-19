# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from threading import Thread
from customtkinter import CTkFrame, CTkLabel, CTkButton
from minecraft_launcher_lib.utils import get_minecraft_news
from minecraft_launcher_lib.types import Articles
from PIL import Image, ImageTk
from io import BytesIO
import requests


class News(CTkFrame):
    articles: Articles

    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.grid_columnconfigure(0, weight=1)

        self.article = CTkLabel(
            master=self,
            height=100,
            fg_color=("white", "gray38"),  # <- custom tuple-color
            text_font=("Roboto Medium", -20),  # font name and size in px
            text="Loading",
        )
        self.article.grid(row=0, column=0, pady=20, padx=20, sticky="nswe")

        self.article_subheader = CTkLabel(master=self, text="Loading")
        self.article_subheader.grid(row=1, column=0, pady=10, padx=10, sticky="nswe")

        self.image = CTkLabel(master=self, text="Loading")
        self.image.grid(row=2, column=0, pady=10, padx=10, sticky="nswe")

        # empty row as spacing
        self.grid_rowconfigure(3, weight=1)

        self.navbar = CTkFrame(master=self)
        self.navbar.grid(row=4, column=0, pady=10, padx=10, sticky="nswe")

        self.prev_button = CTkButton(
            master=self.navbar,
            text="<",
            command=self.decrement_article_index,
        )
        self.prev_button.grid(row=0, column=0, sticky="nswe")

        self.current_article_index = CTkLabel(master=self.navbar, text="1")
        self.current_article_index.grid(row=0, column=1, sticky="nswe")
        self.navbar.grid_columnconfigure(1, weight=1)

        self.next_button = CTkButton(
            master=self.navbar,
            text=">",
            command=self.increment_article_index,
        )
        self.next_button.grid(row=0, column=2, sticky="nswe")

        updater = Thread(target=self.update_news)
        updater.start()

    def update_news(self) -> None:
        self.articles = get_minecraft_news()
        self.update_article()

    def update_article(self) -> None:
        index = int(self.current_article_index.text)
        tile = self.articles["article_grid"][index - 1]["default_tile"]
        self.article.set_text(tile["title"])
        self.article_subheader.set_text(tile["sub_header"])
        self.update_image(index)

    def update_image(self, index) -> None:
        image_url = self.articles["article_grid"][index - 1]["default_tile"]["image"][
            "imageURL"
        ]
        image_url = f"https://www.minecraft.net{image_url}"
        response = requests.get(image_url, headers={"User-Agent": "ice-launcher"})
        image = Image.open(BytesIO(response.content))
        self.photo = ImageTk.PhotoImage(image.resize((200, 200), Image.ANTIALIAS))
        self.image.configure(image=self.photo)

    def decrement_article_index(self) -> None:
        if int(self.current_article_index.text) == 1:
            return

        self.current_article_index.set_text(
            str(int(self.current_article_index.text) - 1)
        )
        self.update_article()

    def increment_article_index(self) -> None:
        if int(self.current_article_index.text) == len(self.articles["article_grid"]):
            return

        self.current_article_index.set_text(
            str(int(self.current_article_index.text) + 1)
        )
        self.update_article()
