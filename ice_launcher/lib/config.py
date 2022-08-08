# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import json
from os import path
from typing import List, TypedDict

from . import dirs

__config_path__: str = path.join(dirs.user_data_dir, "config.json")


class Config(TypedDict):
    config_version: int
    automatically_check_for_updates: bool
    last_used_account: str
    jvm_options: List[str]
    jvm_memory: str


def default() -> Config:
    return {
        "config_version": 1,
        "automatically_check_for_updates": True,
        "last_used_account": "",
        "jvm_options": [],
        "jvm_memory": "2G",
    }


def write(config: Config) -> None:
    with open(__config_path__, "w") as f:
        json.dump(config, f)


def read() -> Config:
    if not path.exists(__config_path__):
        write(default())

    with open(__config_path__, "r") as f:
        config = json.load(f)

    # Update old config with new values
    for key, value in default().items():
        if key not in config:
            config[key] = value

    write(config)
    return config
