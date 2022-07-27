# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import json
from os import path
from typing import TypedDict

from . import dirs

__config_path__: str = path.join(dirs.user_data_dir, "config.json")


class Config(TypedDict):
    config_version: int
    automatically_check_for_updates: bool
    last_used_account: str


def default() -> Config:
    return {
        "config_version": 1,
        "automatically_check_for_updates": True,
        "last_used_account": "",
    }


def write(config: Config) -> None:
    with open(__config_path__, "w") as f:
        json.dump(config, f)


def read() -> Config:
    if not path.exists(__config_path__):
        write(default())

    with open(__config_path__, "r") as f:
        return json.load(f)
