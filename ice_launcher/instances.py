# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from customtkinter import CTkButton, CTkFrame, CTkLabel

from .lib import instances
from .new_instance import NewInstance


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

        self.instances_list = CTkFrame(master=self)
        self.instances_list.grid(row=1, column=0, pady=10, padx=10, sticky="nswe")
        self.instances_list.grid_columnconfigure(1, weight=1)

        # empty row as spacing
        self.grid_rowconfigure(2, weight=1)

        self.add_account_button = CTkButton(
            master=self,
            text="New Instance",
            command=self.add_new_instance,
        )
        self.add_account_button.grid(row=3, column=0, pady=20, padx=20)

        self.update_instance_list()

    def add_new_instance(self) -> None:
        self.new_instance_window = NewInstance(master=self)
        self.new_instance_window.protocol(
            "WM_DELETE_WINDOW", self.on_closing_new_instance_window
        )

    def on_closing_new_instance_window(self, event=0) -> None:
        self.new_instance_window.destroy()
        self.update_instance_list()

    def update_instance_list(self) -> None:
        for instance in self.instances_list.winfo_children():
            instance.destroy()

        for index, instance_name in enumerate(instances.list()):
            label = CTkLabel(master=self.instances_list, text=instance_name)
            label.grid(row=index, column=0, pady=10, padx=10, sticky="nswe")
            launch_button = CTkButton(
                master=self.instances_list,
                text="Launch",
                command=lambda: instances.launch(instance_name),
            )
            launch_button.grid(row=index, column=1, pady=10, padx=10, sticky="e")
