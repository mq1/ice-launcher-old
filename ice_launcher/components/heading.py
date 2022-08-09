# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from customtkinter import CTkFrame, CTkLabel


class Heading(CTkFrame):
    def __init__(self, master, text: str, *args, **kwargs) -> None:
        super().__init__(master, fg_color="gray38", *args, **kwargs)

        self.label = CTkLabel(
            master=self,
            text_font=("Roboto Medium", 30),  # type: ignore
            text=text,
            anchor="w",
        )
        self.label.grid(row=0, column=0, pady=20, padx=20, sticky="nswe")
