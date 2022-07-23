# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from customtkinter import CTkFrame, CTkLabel, CTkButton
from os import listdir, path, makedirs
from typing import List
from ice_launcher import dirs
from ice_launcher.new_instance import NewInstance
from ice_launcher import accounts
from ice_launcher.__about__ import __version__
from minecraft_launcher_lib.command import get_minecraft_command
from minecraft_launcher_lib.types import MinecraftOptions
import json
import subprocess
from ice_launcher.new_instance import InstanceJson


__instances_dir__: str = path.join(dirs.user_data_dir, "instances")


def get_instance_list() -> List[str]:
    # check if instances folder exists
    if not path.exists(__instances_dir__):
        makedirs(__instances_dir__)

    list = listdir(__instances_dir__)
    if ".DS_Store" in list:
        list.remove(".DS_Store")

    return list


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

        for index, instance_name in enumerate(get_instance_list()):
            label = CTkLabel(master=self.instances_list, text=instance_name)
            label.grid(row=index, column=0, pady=10, padx=10, sticky="nswe")
            launch_button = CTkButton(
                master=self.instances_list,
                text="Launch",
                command=lambda: self.launch_instance(instance_name),
            )
            launch_button.grid(row=index, column=1, pady=10, padx=10, sticky="e")
    
    def launch_instance(self, instance_name: str) -> None:
        # TODO: account selection
        account = accounts.read_document()["accounts"][0]

        options: MinecraftOptions = {
            "username": account["name"],
            "uuid": account["id"],
            "token": account["access_token"],
            "jvmArguments": ["-Xmx2G", "-Xms2G"],
            "launcherName": "Ice Launcher",
            "launcherVersion": __version__,
            "gameDirectory": path.join(__instances_dir__, instance_name),
        }

        instance_dir = path.join(__instances_dir__, instance_name)
        with open(path.join(instance_dir, "instance.json"), "r") as f:
            instance_json: InstanceJson = json.load(f)

        minecraft_command = get_minecraft_command(instance_json["minecraft_version"], dirs.user_data_dir, options)
        subprocess.call(minecraft_command)
