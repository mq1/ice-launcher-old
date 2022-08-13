# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from os import path

import tomli
import tomli_w
from pydantic import BaseModel

from . import dirs

__config_path__: str = path.join(dirs.user_data_dir, "config.toml")


class Config(BaseModel):
    config_version: int = 1
    automatically_check_for_updates: bool = True
    jvm_options: list[str] = []
    jvm_memory: str = "2G"


def write(config: Config) -> None:
    with open(__config_path__, "wb") as f:
        tomli_w.dump(config.dict(), f)


def read() -> Config:
    if not path.exists(__config_path__):
        return Config()

    with open(__config_path__, "rb") as f:
        config = Config.parse_obj(tomli.load(f))

    # Writes the config file in case it is outdated.
    write(config)

    return config
