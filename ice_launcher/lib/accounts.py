# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from threading import Thread
from typing import Any, Optional

import tomli
import tomli_w
from pydantic import BaseModel

from . import ACCOUNTS_FILE_PATH, msa


class Document(BaseModel):
    version: int = 1
    active_account: str = ""
    accounts: dict[str, msa.Account] = {}


def _write_document(doc: Document) -> None:
    with open(ACCOUNTS_FILE_PATH, "wb") as f:
        tomli_w.dump(doc.dict(), f)


def _read_document() -> Document:
    if not path.exists(ACCOUNTS_FILE_PATH):
        return Document()

    with open(ACCOUNTS_FILE_PATH, "rb") as f:
        doc = Document.parse_obj(tomli.load(f))

    # Writes the document file in case it is outdated.
    _write_document(doc)

    return doc


def get_accounts() -> dict[str, msa.Account]:
    doc = _read_document()

    return doc.accounts


class CallbackHandler(BaseHTTPRequestHandler):
    state: str
    code_verifier: str
    callback_function: Any

    def do_GET(self) -> None:
        account_entry = msa.login(self.path, self.state, self.code_verifier)
        add_account(account_entry)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Login</title></head>")
        self.wfile.write(b"<body><p>You have been logged in.</p>")
        self.wfile.write(b"<p>You can close this window.</p>")
        self.wfile.write(b"</body></html>")

        self.callback_function()
        Thread(target=self.server.shutdown).start()


def login_account(callback_function: Any) -> None:
    login_data = msa.get_login_data()

    webbrowser.open(login_data.uri)
    handler = CallbackHandler
    handler.state = login_data.state
    handler.code_verifier = login_data.code_verifier
    handler.callback_function = callback_function
    httpd = HTTPServer(("127.0.0.1", 3003), handler)
    httpd.serve_forever()


def add_account(account_entry: msa.AccountEntry) -> None:
    doc = _read_document()
    doc.accounts[account_entry.minecraft_id] = account_entry.account
    _write_document(doc)


def remove_account(account_id: str) -> None:
    doc = _read_document()

    del doc.accounts[account_id]
    if doc.active_account == account_id:
        doc.active_account = ""

    _write_document(doc)


def refresh_account(account_id: str) -> msa.Account:
    doc = _read_document()

    account = doc.accounts[account_id]
    account = msa.refresh(account)
    doc.accounts[account_id] = account

    _write_document(doc)

    return account


def get_active_account() -> Optional[msa.AccountEntry]:
    doc = _read_document()
    id = doc.active_account

    if id == "":
        return None

    account_entry = msa.AccountEntry(
        minecraft_id=id,
        account=doc.accounts[id],
    )

    return account_entry


def set_active_account(account_id: str) -> None:
    doc = _read_document()
    doc.active_account = account_id
    _write_document(doc)


def is_active_account(account_id: str) -> bool:
    doc = _read_document()

    return doc.active_account == account_id
