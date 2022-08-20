# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from tkinter import messagebox, ttk

from customtkinter import CTkButton, CTkFrame, CTkLabel

from ice_launcher.components.heading import Heading
from ice_launcher.components.scrollable_frame import ScrollableFrame
from ice_launcher.lib import accounts, msa


class Accounts(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.grid_columnconfigure(0, weight=1)

        heading = Heading(self, "👥 Accounts")
        heading.grid(row=0, column=0, pady=20, padx=20, sticky="nwe")

        self.accounts_list = ScrollableFrame(master=self)
        self.accounts_list.grid(row=1, column=0, pady=20, padx=20, sticky="nswe")
        self.grid_rowconfigure(1, weight=1)

        button_bar = CTkFrame(master=self)
        button_bar.grid(row=100, column=0, pady=0, padx=0, sticky="nwe")

        add_account_button = CTkButton(
            master=button_bar,
            text="Add Account ✨",
            command=self.add_account,
        )
        add_account_button.grid(row=0, column=0, pady=10, padx=10, sticky="nse")
        button_bar.grid_columnconfigure(1, weight=1)

        self.update_accounts_list()

    def add_account(self) -> None:
        accounts.login_account(self.update_accounts_list)

    def select_account(self, account_id: str) -> None:
        accounts.set_active_account(account_id)
        self.update_accounts_list()

    def remove_account(self, account_id: str) -> None:
        if messagebox.askyesno(
            "Remove account", "Are you sure you want to remove this account?"
        ):
            accounts.remove_account(account_id)
            self.update_accounts_list()

    def add_account_to_list(
        self, index: int, account_id: str, account: msa.Account
    ) -> None:
        emoji = "✅" if accounts.is_active_account(account_id) else "👤"

        label = CTkLabel(
            master=self.accounts_list.content,
            text=f"{emoji} {account.minecraft_username}",
            anchor="w",
        )
        label.grid(row=index, column=0, pady=10, padx=0, sticky="nsw")
        remove_button = CTkButton(
            master=self.accounts_list.content,
            text="Remove 💣",
            width=0,
            command=lambda: self.remove_account(account_id),
        )
        remove_button.grid(row=index, column=1, pady=10, padx=10, sticky="nse")
        select_button = CTkButton(
            master=self.accounts_list.content,
            text="Select ✅",
            width=0,
            command=lambda: self.select_account(account_id),
        )
        select_button.grid(row=index, column=2, pady=10, padx=(0, 10), sticky="nse")

    def update_accounts_list(self) -> None:
        for account in self.accounts_list.content.winfo_children():
            account.destroy()

        for index, (account_id, account) in enumerate(accounts.get_accounts().items()):
            self.add_account_to_list(index * 2, account_id, account)

            separator = ttk.Separator(self.accounts_list.content, orient="horizontal")
            separator.grid(
                row=index * 2 + 1,
                column=0,
                columnspan=3,
                pady=0,
                padx=(0, 10),
                sticky="ew",
            )
