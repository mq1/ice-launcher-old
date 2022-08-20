# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from tkinter import messagebox

from customtkinter import CTkButton, CTkFrame, CTkInputDialog

from ice_launcher import views
from ice_launcher.components.heading import Heading
from ice_launcher.lib import instances


class EditInstance(CTkFrame):
    def __init__(self, master, instance_name: str) -> None:
        super().__init__(master=master)
        self.grid_columnconfigure(0, weight=1)

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
            text="Delete 💣",
            command=self.delete_instance,
        )
        delete_button.grid(row=0, column=2, pady=10, padx=10, sticky="nse")

    def rename_instance(self):
        dialog = CTkInputDialog(
            master=None,
            text="Type a new name for the instance",
            title="Rename Instance",
        )
        new_name = dialog.get_input()
        if new_name:
            instances.rename(self.heading.label.text, new_name)
            self.heading.label.configure(text=new_name)

    def done(self):
        self.master.open_page(None, views.Instances(master=self.master))  # type: ignore

    def delete_instance(self) -> None:
        if messagebox.askyesno(
            "Delete Instance",
            f"Are you sure you want to delete the instance {self.heading.label.text}?",
        ):
            instances.delete(self.heading.label.text)
            self.master.open_page(None, views.Instances(master=self.master))  # type: ignore
