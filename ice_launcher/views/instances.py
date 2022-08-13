# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from subprocess import Popen
from tkinter import ttk

from customtkinter import CTkButton, CTkFrame, CTkLabel

from ice_launcher.components.heading import Heading
from ice_launcher.components.scrollable_frame import ScrollableFrame
from ice_launcher.lib import accounts, instances
from ice_launcher.views import EditInstance, Logs, NewInstance


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

        self.account_label = CTkLabel(
            master=status_bar,
            text="",
            anchor="e",
        )
        self.account_label.grid(row=0, column=2, pady=0, padx=10, sticky="nse")

        self.update_selected_account()
        self.update_instance_list()

    def add_new_instance(self) -> None:
        self.master.open_page(None, NewInstance(master=self.master))  # type: ignore

    def edit_instance(self, instance_name: str) -> None:
        self.master.open_page(None, EditInstance(master=self.master, instance_name=instance_name))  # type: ignore

    def launch_instance(self, instance_name: str) -> None:
        self.master.open_page(None, Logs(master=self.master))  # type: ignore

        def show_logs(process: Popen):
            self.master.current_page.update_logs(process)  # type: ignore

        if self.selected_account is not None:
            instances.launch(instance_name, self.selected_account[0], show_logs)

    def update_selected_account(self) -> None:
        self.selected_account = accounts.get_active_account()

        if self.selected_account is None:
            account_name = "You need to select an account first"
        else:
            account_name = f"Account: {self.selected_account[1].name}"

        self.account_label.configure(text=account_name)

    def add_instance_to_list(self, index: int, instance_name: str) -> None:
        instance_emoji = "⛏"

        info = instances.get_info(instance_name)
        match info["instance_type"]:
            case instances.InstanceType.fabric:
                instance_emoji = "🧵"
            case instances.InstanceType.forge:
                instance_emoji = "⚒️"

        label = CTkLabel(
            master=self.instances_list.content,
            text=f"{instance_emoji} {instance_name}",
            anchor="w",
        )
        label.grid(row=index, column=0, pady=10, padx=0, sticky="nsw")
        edit_button = CTkButton(
            master=self.instances_list.content,
            text="Edit ⚙️",
            width=0,
            command=lambda: self.edit_instance(instance_name),
        )
        edit_button.grid(row=index, column=1, pady=10, padx=0, sticky="nse")

        if self.selected_account is not None:
            launch_button = CTkButton(
                master=self.instances_list.content,
                text="Launch 🚀",
                width=0,
                command=lambda: self.launch_instance(instance_name),
            )
            launch_button.grid(row=index, column=2, pady=10, padx=10, sticky="nse")

    def update_instance_list(self) -> None:
        instance_list = instances.list()

        for instance in self.instances_list.content.winfo_children():
            instance.destroy()

        for index, instance_name in enumerate(instance_list):
            self.add_instance_to_list(index * 2, instance_name)

            separator = ttk.Separator(self.instances_list.content, orient="horizontal")
            separator.grid(
                row=index * 2 + 1,
                column=0,
                columnspan=3,
                pady=0,
                padx=(0, 10),
                sticky="ew",
            )
