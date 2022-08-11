# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from os import path
from typing import Any, TypedDict, cast

import tomli
import tomli_w
from minecraft_launcher_lib.microsoft_types import CompleteLoginResponse

from . import dirs

__accounts_file__: str = path.join(dirs.user_data_dir, "accounts.toml")


class Document(TypedDict):
    version: int
    accounts: dict[str, CompleteLoginResponse]


def new_document() -> Document:
    doc: Document = {"version": 1, "accounts": {}}

    write_document(doc)

    return doc


def read_document() -> Document:
    if not path.exists(__accounts_file__):
        doc = new_document()

    with open(__accounts_file__, "rb") as f:
        doc = cast(Document, tomli.load(f))

    return doc


def write_document(doc: Document) -> None:
    with open(__accounts_file__, "wb") as f:
        tomli_w.dump(cast(dict[str, Any], doc), f)
