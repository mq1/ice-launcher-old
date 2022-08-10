# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from tkinter import ttk

from customtkinter import CTkButton, CTkFrame, CTkLabel
from minecraft_launcher_lib import microsoft_account as msa

from ice_launcher.components.heading import Heading
from ice_launcher.components.scrollable_frame import ScrollableFrame
from ice_launcher.lib import accounts

__client_id__: str = "0018ddff-bd2f-4cc6-b220-66f6a4462a5c"
__redirect_uri__: str = "http://localhost:3003"


class CallbackHandler(BaseHTTPRequestHandler):
    state: str
    code_verifier: str

    def do_GET(self) -> None:
        auth_code = msa.parse_auth_code_url(self.path, self.state)

        login_data = msa.complete_login(
            client_id=__client_id__,
            client_secret=None,
            redirect_uri=__redirect_uri__,
            auth_code=auth_code,
            code_verifier=self.code_verifier,
        )

        doc = accounts.read_document()
        doc["accounts"].append(login_data)
        accounts.write_document(doc)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Login</title></head>")
        self.wfile.write(b"<body><p>You have been logged in.</p>")
        self.wfile.write(b"<p>You can close this window.</p>")
        self.wfile.write(b"</body></html>")

        Thread(target=self.server.shutdown).start()


class Accounts(CTkFrame):
    doc: accounts.Document

    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.grid_columnconfigure(0, weight=1)

        self.doc = accounts.read_document()

        heading = Heading(self, "👥 Accounts")
        heading.grid(row=0, column=0, pady=20, padx=20, sticky="nwe")

        self.accounts_list = ScrollableFrame(master=self)
        self.accounts_list.grid(row=1, column=0, pady=20, padx=20, sticky="nswe")
        self.grid_rowconfigure(1, weight=1)

        self.update_accounts_list()

    def add_account(self) -> None:
        login_url, state, code_verifier = msa.get_secure_login_data(
            __client_id__, __redirect_uri__
        )

        webbrowser.open(login_url)
        handler = CallbackHandler
        handler.state = state
        handler.code_verifier = code_verifier
        httpd = HTTPServer(("127.0.0.1", 3003), handler)
        httpd.serve_forever()
        self.update_accounts_list()

    def delete_account(self, index) -> None:
        del self.doc["accounts"][index]
        accounts.write_document(self.doc)
        self.update_accounts_list()

    def update_accounts_list(self) -> None:
        for account in self.accounts_list.content.winfo_children():
            account.destroy()

        for index, account in enumerate(self.doc["accounts"]):
            label = CTkLabel(
                master=self.accounts_list.content,
                text=f"👤 {account['name']}",
                anchor="w",
            )
            label.grid(row=index * 2, column=0, pady=10, padx=0, sticky="nw")
            delete_button = CTkButton(
                master=self.accounts_list.content,
                text="Delete 💣",
                width=0,
                command=lambda index=index: self.delete_account(index),
            )
            delete_button.grid(
                row=index * 2, column=1, pady=10, padx=(0, 10), sticky="e"
            )
            separator = ttk.Separator(self.accounts_list.content, orient="horizontal")
            separator.grid(
                row=index * 2 + 1,
                column=0,
                columnspan=2,
                pady=0,
                padx=(0, 10),
                sticky="ew",
            )

        add_account_button = CTkButton(
            master=self.accounts_list.content,
            text="Add Account ✨",
            command=self.add_account,
        )
        add_account_button.grid(
            row=len(self.doc["accounts"]) * 2, column=0, pady=20, padx=0, sticky="nw"
        )
