from customtkinter import CTk, CTkButton, CTkFrame
from news import News
from settings import Settings
from about import About


class App(CTk):
    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("PyMinecraftLauncher")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.navigator = CTkFrame(width=180, corner_radius=0, master=self)
        self.navigator.pack(fill="y", side="left")

        self.news_button = CTkButton(
            master=self.navigator, text="News", command=self.open_news
        )
        self.news_button.pack(pady=(20, 10), padx=20, side="top")

        self.settings_button = CTkButton(
            master=self.navigator, text="Settings", command=self.open_settings
        )
        self.settings_button.pack(pady=10, padx=20, side="top")

        self.about_button = CTkButton(
            master=self.navigator, text="About", command=self.open_about
        )
        self.about_button.pack(pady=(10, 20), padx=20, side="bottom")

        self.main_frame = News(master=self)
        self.main_frame.pack(fill="both", expand=True, pady=20, padx=20)

    def on_closing(self, event=0):
        self.destroy()

    def open_news(self):
        self.main_frame.destroy()
        self.main_frame = News(master=self)
        self.main_frame.pack(fill="both", expand=True, pady=20, padx=20)

    def open_settings(self):
        self.main_frame.destroy()
        self.main_frame = Settings(master=self)
        self.main_frame.pack(fill="both", expand=True, pady=20, padx=20)

    def open_about(self):
        self.main_frame.destroy()
        self.main_frame = About(master=self)
        self.main_frame.pack(fill="both", expand=True, pady=20, padx=20)

    def button_event(self):
        print("Button pressed")


if __name__ == "__main__":
    app = App()
    app.mainloop()
