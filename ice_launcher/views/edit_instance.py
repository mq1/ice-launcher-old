# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from customtkinter import CTkButton, CTkFrame, CTkInputDialog, CTkToplevel, StringVar

from ice_launcher.components.heading import Heading
from ice_launcher.lib import instances


class EditInstance(CTkToplevel):
    def __init__(self, instance_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_name = instance_name
        self.title(instance_name)

        self.heading = Heading(master=self, text=instance_name)
        self.heading.grid(row=0, column=0, pady=20, padx=20, sticky="nwe")

        # empty row as spacing
        self.grid_rowconfigure(99, weight=1)

        button_bar = CTkFrame(master=self)
        button_bar.grid(row=100, column=0, pady=20, padx=20, sticky="swe")

        # empty column as spacing
        button_bar.grid_columnconfigure(0, weight=1)

        rename_button = CTkButton(
            master=button_bar,
            text="Rename 📝",
            command=self.rename_instance,
        )
        rename_button.grid(row=0, column=1, pady=10, padx=10, sticky="nse")

        delete_button = CTkButton(
            master=button_bar,
            text="Delete 🗑️",
            command=self.delete_instance,
        )
        delete_button.grid(row=0, column=2, pady=10, padx=10, sticky="nse")

    def rename_instance(self):
        dialog = CTkInputDialog(
            master=None,
            text="Type a new name for the instance",
            title="Rename Instance",
        )
        new_name = f"{dialog.get_input()}"
        instances.rename(self.instance_name, new_name)
        self.instance_name = new_name
        self.title(new_name)
        self.heading.label.configure(text=new_name)
        self.master.update_instance_list()  # type: ignore

    def delete_instance(self) -> None:
        instances.delete(self.instance_name)
        self.master.update_instance_list()  # type: ignore
        self.destroy()
