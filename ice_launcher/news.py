from customtkinter import CTkFrame, CTkLabel, CTkButton
from minecraft_launcher_lib.utils import get_minecraft_news


class News(CTkFrame):
    articles = get_minecraft_news()

    def __init__(self, master):
        super().__init__(master=master)

        self.article = CTkLabel(
            master=self,
            height=100,
            fg_color=("white", "gray38"),  # <- custom tuple-color
            text_font=("Roboto Medium", -20),  # font name and size in px
        )
        self.article.pack(pady=20, padx=20, fill="x")

        self.article_subheader = CTkLabel(master=self)
        self.article_subheader.pack()

        self.navbar = CTkFrame(master=self)
        self.navbar.pack(side="bottom", fill="x", pady=10, padx=10)

        self.prev_button = CTkButton(
            master=self.navbar,
            text="<",
            command=self.decrement_article_index,
        )
        self.prev_button.pack(side="left")

        self.current_article_index = CTkLabel(master=self.navbar, text="1")
        self.current_article_index.pack(expand=True, fill="x", side="left")

        self.next_button = CTkButton(
            master=self.navbar,
            text=">",
            command=self.increment_article_index,
        )
        self.next_button.pack(side="right")

        self.update_article()

    def update_article(self):
        index = int(self.current_article_index.text)
        tile = self.articles["article_grid"][index - 1]["default_tile"]
        self.article.set_text(tile["title"])
        self.article_subheader.set_text(tile["sub_header"])
        
    def decrement_article_index(self):
        if int(self.current_article_index.text) == 1:
            return

        self.current_article_index.set_text(
            str(int(self.current_article_index.text) - 1)
        )
        self.update_article()

    def increment_article_index(self):
        if int(self.current_article_index.text) == len(self.articles["article_grid"]):
            return

        self.current_article_index.set_text(
            str(int(self.current_article_index.text) + 1)
        )
        self.update_article()
