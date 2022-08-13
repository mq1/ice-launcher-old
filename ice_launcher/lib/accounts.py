# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import webbrowser
from enum import Enum
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from threading import Thread
from typing import Any, Optional

import tomli
import tomli_w
from minecraft_launcher_lib import microsoft_account as msa
from minecraft_launcher_lib import microsoft_types
from pydantic import BaseModel

from . import __client_id__, dirs

__accounts_file__: str = path.join(dirs.user_data_dir, "accounts.toml")
__redirect_uri__: str = "http://localhost:3003"


class _State(str, Enum):
    active = "ACTIVE"
    inactive = "INACTIVE"


class _MinecraftProfileInfo(BaseModel):
    state: _State
    url: str


class _MinecraftProfileSkin(_MinecraftProfileInfo):
    variant: str


class _MinecraftProfileCape(_MinecraftProfileInfo):
    alias: str


class CompleteLoginResponse(BaseModel):
    name: str
    skins: dict[str, _MinecraftProfileSkin]
    capes: dict[str, _MinecraftProfileCape]
    access_token: str
    refresh_token: str


class Document(BaseModel):
    version: int = 1
    active_account: str = ""
    accounts: dict[str, CompleteLoginResponse] = {}


def convert_account_type(
    account: microsoft_types.CompleteLoginResponse,
) -> CompleteLoginResponse:
    skins: dict[str, _MinecraftProfileSkin] = {}
    for skin in account["skins"]:
        skins[skin["id"]] = _MinecraftProfileSkin.parse_obj(skin)

    capes: dict[str, _MinecraftProfileCape] = {}
    for cape in account["capes"]:
        capes[cape["id"]] = _MinecraftProfileCape.parse_obj(cape)

    converted_account = CompleteLoginResponse(
        **{
            "name": account["name"],
            "skins": skins,
            "capes": capes,
            "access_token": account["access_token"],
            "refresh_token": account["refresh_token"],
        }
    )

    return converted_account


def _write_document(doc: Document) -> None:
    with open(__accounts_file__, "wb") as f:
        tomli_w.dump(doc.dict(), f)


def _read_document() -> Document:
    if not path.exists(__accounts_file__):
        return Document()

    with open(__accounts_file__, "rb") as f:
        doc = Document.parse_obj(tomli.load(f))

    # Writes the document file in case it is outdated.
    _write_document(doc)

    return doc


def get_accounts() -> dict[str, CompleteLoginResponse]:
    doc = _read_document()

    return doc.accounts


class CallbackHandler(BaseHTTPRequestHandler):
    state: str
    code_verifier: str
    callback_function: Any

    def do_GET(self) -> None:
        auth_code = msa.parse_auth_code_url(self.path, self.state)

        login_data = msa.complete_login(
            client_id=__client_id__,
            client_secret=None,
            redirect_uri=__redirect_uri__,
            auth_code=auth_code,
            code_verifier=self.code_verifier,
        )

        converted_login_data = add_account(login_data)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Login</title></head>")
        self.wfile.write(b"<body><p>You have been logged in.</p>")
        self.wfile.write(b"<p>You can close this window.</p>")
        self.wfile.write(b"</body></html>")

        self.callback_function(login_data["id"], converted_login_data)
        Thread(target=self.server.shutdown).start()


def login_account(callback_function: Any) -> None:
    login_url, state, code_verifier = msa.get_secure_login_data(
        __client_id__, __redirect_uri__
    )

    webbrowser.open(login_url)
    handler = CallbackHandler
    handler.state = state
    handler.code_verifier = code_verifier
    handler.callback_function = callback_function
    httpd = HTTPServer(("127.0.0.1", 3003), handler)
    httpd.serve_forever()


def add_account(
    login_data: microsoft_types.CompleteLoginResponse,
) -> CompleteLoginResponse:
    converted_login_data = convert_account_type(login_data)

    doc = _read_document()

    doc.accounts[login_data["id"]] = converted_login_data

    _write_document(doc)

    return converted_login_data


def remove_account(account_id: str) -> None:
    doc = _read_document()

    del doc.accounts[account_id]
    if doc.active_account == account_id:
        doc.active_account = ""

    _write_document(doc)


def refresh_account(account_id: str) -> CompleteLoginResponse:
    doc = _read_document()

    account = doc.accounts[account_id]

    account = msa.complete_refresh(
        client_id=__client_id__,
        client_secret=None,
        redirect_uri=None,
        refresh_token=account.refresh_token,
    )
    converted_account = convert_account_type(account)

    doc.accounts[account_id] = converted_account
    _write_document(doc)

    return converted_account


def get_active_account() -> Optional[tuple[str, CompleteLoginResponse]]:
    doc = _read_document()
    id = doc.active_account

    if id == "":
        return None

    return id, doc.accounts[id]


def set_active_account(account_id: str) -> None:
    doc = _read_document()

    doc.active_account = account_id

    _write_document(doc)


def is_active_account(account_id: str) -> bool:
    doc = _read_document()

    return doc.active_account == account_id
