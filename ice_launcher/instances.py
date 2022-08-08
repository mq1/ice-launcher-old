# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from tkinter import ttk

from customtkinter import CTkButton, CTkComboBox, CTkFrame, CTkLabel, StringVar

from .__about__ import __version__
from .components.heading import Heading
from .components.scrollable_frame import ScrollableFrame
from .lib import accounts, config, instances
from .new_instance import NewInstance


class Instances(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.account_list = [a["name"] for a in accounts.read_document()["accounts"]]

        self.grid_columnconfigure(0, weight=1)

        heading = Heading(master=self, text="Instances")
        heading.grid(row=0, column=0, pady=20, padx=20, sticky="nwe")

        self.instances_list = ScrollableFrame(master=self)
        self.instances_list.grid(row=1, column=0, pady=20, padx=20, sticky="nswe")
        self.grid_rowconfigure(1, weight=1)

        status_bar = CTkFrame(master=self)
        status_bar.grid(row=100, column=0, pady=0, padx=0, sticky="swe")

        # empty column as spacing
        status_bar.grid_columnconfigure(0, weight=1)

        account_label = CTkLabel(master=status_bar, text="Account:", anchor="e")
        account_label.grid(row=0, column=1, pady=0, padx=0, sticky="nse")

        self.selected_account = StringVar()
        account_selector = CTkComboBox(
            master=status_bar,
            values=self.account_list,
            command=lambda _: self.update_account_list(),
            variable=self.selected_account,
        )
        account_selector.grid(row=0, column=2, pady=10, padx=10, sticky="e")

        self.update_instance_list()
        self.set_default_account()
        self.update_account_list()

    def add_new_instance(self) -> None:
        self.new_instance_window = NewInstance(master=self)
        self.new_instance_window.protocol(
            "WM_DELETE_WINDOW", self.on_closing_new_instance_window
        )

    def on_closing_new_instance_window(self, event=0) -> None:
        self.new_instance_window.destroy()
        self.update_instance_list()

    def update_instance_list(self) -> None:
        instance_list = instances.list()

        for instance in self.instances_list.content.winfo_children():
            instance.destroy()

        for index, instance_name in enumerate(instance_list):
            label = CTkLabel(
                master=self.instances_list.content, text=instance_name, anchor="w"
            )
            label.grid(row=index * 2, column=0, pady=10, padx=10, sticky="nw")
            launch_button = CTkButton(
                master=self.instances_list.content,
                text="Launch",
                command=lambda: instances.launch(
                    instance_name, self.selected_account.get(), __version__
                ),
            )
            launch_button.grid(row=index * 2, column=1, pady=10, padx=10, sticky="e")
            separator = ttk.Separator(self.instances_list.content, orient="horizontal")
            separator.grid(
                row=index * 2 + 1, column=0, columnspan=2, pady=0, padx=10, sticky="ew"
            )

        new_instance_button = CTkButton(
            master=self.instances_list.content,
            text="New Instance",
            command=self.add_new_instance,
        )
        new_instance_button.grid(
            row=len(instance_list) * 2, column=0, pady=20, padx=10, sticky="nw"
        )

    def set_default_account(self) -> None:
        c = config.read()
        if c["last_used_account"] != "":
            self.selected_account.set(c["last_used_account"])
        elif len(self.account_list) > 0:
            self.selected_account.set(self.account_list[0])

    def update_account_list(self) -> None:
        self.account_list = [a["name"] for a in accounts.read_document()["accounts"]]

        # update last used account
        c = config.read()
        c["last_used_account"] = self.selected_account.get()
        config.write(c)
