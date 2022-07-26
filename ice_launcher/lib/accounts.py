# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import json
from os import path
from typing import List, TypedDict

from minecraft_launcher_lib.microsoft_types import CompleteLoginResponse

from . import dirs

__accounts_file__: str = path.join(dirs.user_data_dir, "accounts.json")


class Document(TypedDict):
    version: int
    accounts: List[CompleteLoginResponse]


def new_document() -> Document:
    doc: Document = {"version": 1, "accounts": []}

    write_document(doc)

    return doc


def read_document() -> Document:
    if not path.exists(__accounts_file__):
        doc = new_document()

    with open(__accounts_file__, "r") as f:
        doc = json.load(f)

    return doc


def write_document(doc: Document) -> None:
    with open(__accounts_file__, "w") as f:
        json.dump(doc, f)
