# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from customtkinter import CTkFrame, CTkLabel
from os import listdir, path, makedirs
from typing import List


def get_instance_list() -> List[str]:
    # check if instances folder exists
    if not path.exists("instances"):
        makedirs("instances")

    return listdir("instances")


class Instances(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.grid_columnconfigure(0, weight=1)

        self.app_name = CTkLabel(
            master=self,
            height=100,
            fg_color=("white", "gray38"),  # <- custom tuple-color
            text_font=("Roboto Medium", -20),  # font name and size in px
            text="Instances",
        )
        self.app_name.grid(row=0, column=0, pady=20, padx=20, sticky="nswe")

        self.instances = CTkFrame(master=self)
        self.instances.grid(row=1, column=0, pady=10, padx=10, sticky="nswe")

        self.update_instance_list()

    def update_instance_list(self) -> None:
        for instance in self.instances.winfo_children():
            instance.destroy()

        for index, instance in enumerate(get_instance_list()):
            label = CTkLabel(master=self.instances, text=instance)
            label.grid(row=index, column=0, sticky="nswe")
