# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from tkinter import ttk
from typing import Optional

from customtkinter import CTkButton, CTkFrame, CTkLabel, StringVar

from ice_launcher.components.heading import Heading
from ice_launcher.components.scrollable_frame import ScrollableFrame
from ice_launcher.lib import accounts, instances
from ice_launcher.views.edit_instance import EditInstance


class Instances(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.account_list = list(accounts.get_accounts().keys())

        self.grid_columnconfigure(0, weight=1)

        heading = Heading(master=self, text="🧊 Instances")
        heading.grid(row=0, column=0, pady=20, padx=20, sticky="nwe")

        self.instances_list = ScrollableFrame(master=self)
        self.instances_list.grid(row=1, column=0, pady=20, padx=20, sticky="nswe")
        self.grid_rowconfigure(1, weight=1)

        status_bar = CTkFrame(master=self)
        status_bar.grid(row=100, column=0, pady=0, padx=0, sticky="swe")

        new_instance_button = CTkButton(
            master=status_bar,
            text="New Instance ✨",
            command=self.add_new_instance,
        )
        new_instance_button.grid(row=0, column=0, pady=10, padx=10, sticky="nsw")

        # empty column as spacing
        status_bar.grid_columnconfigure(1, weight=1)

        self.account_var = StringVar()
        account_label = CTkLabel(
            master=status_bar,
            textvariable=self.account_var,
            anchor="e",
        )
        account_label.grid(row=0, column=2, pady=0, padx=10, sticky="nse")

        self.update_selected_account()
        # self.update_instance_list() is called in update_selected_account()

    def add_new_instance(self) -> None:
        self.master.open_view("new_instance")  # type: ignore

    def update_selected_account(self) -> None:
        account = accounts.get_active_account()
        if account is None:
            account_name = "You need to select an account first"
        else:
            account_name = f"Account: {account[1]['name']}"

        self.account_var.set(account_name)

        account_id = account[0] if account is not None else None
        self.update_instance_list(account_id)

    def update_instance_list(self, account_id: Optional[str]) -> None:
        instance_list = instances.list()

        for instance in self.instances_list.content.winfo_children():
            instance.destroy()

        for index, instance_name in enumerate(instance_list):
            instance_emoji = "⛏"

            info = instances.get_info(instance_name)
            match info["instance_type"]:
                case instances.InstanceType.FABRIC:
                    instance_emoji = "🧵"
                case instances.InstanceType.FORGE:
                    instance_emoji = "⚒️"

            label = CTkLabel(
                master=self.instances_list.content,
                text=f"{instance_emoji} {instance_name}",
                anchor="w",
            )
            label.grid(row=index * 2, column=0, pady=10, padx=0, sticky="nsw")
            edit_button = CTkButton(
                master=self.instances_list.content,
                text="Edit ⚙️",
                width=0,
                command=lambda: EditInstance(master=self, instance_name=instance_name),
            )
            edit_button.grid(row=index * 2, column=1, pady=10, padx=0, sticky="nse")

            if account_id is not None:
                launch_button = CTkButton(
                    master=self.instances_list.content,
                    text="Launch 🚀",
                    width=0,
                    command=lambda: instances.launch(instance_name, account_id),
                )
                launch_button.grid(
                    row=index * 2, column=2, pady=10, padx=10, sticky="nse"
                )
            separator = ttk.Separator(self.instances_list.content, orient="horizontal")
            separator.grid(
                row=index * 2 + 1,
                column=0,
                columnspan=3,
                pady=0,
                padx=(0, 10),
                sticky="ew",
            )
