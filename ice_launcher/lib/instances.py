# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import json
import subprocess
from enum import Enum
from os import listdir, makedirs, path
from os import rename as mv
from shutil import rmtree
from threading import Thread
from typing import Any

import tomli
import tomli_w
from pydantic import BaseModel

from . import ProgressCallbacks, __version__, accounts, dirs, launcher_config
from .minecraft_version_meta import install_version
from .minecraft_versions import MinecraftVersionInfo

__INSTANCES_DIR__: str = path.join(dirs.user_data_dir, "instances")


class InstanceType(str, Enum):
    vanilla = "vanilla"
    fabric = "fabric"
    forge = "forge"


class InstanceInfo(BaseModel):
    config_version: int = 1
    instance_type: InstanceType = InstanceType.vanilla
    minecraft_version: str = ""


def list() -> list[str]:
    # check if instances folder exists
    if not path.exists(__INSTANCES_DIR__):
        makedirs(__INSTANCES_DIR__)

    list = [
        x
        for x in listdir(__INSTANCES_DIR__)
        if path.isdir(path.join(__INSTANCES_DIR__, x))
    ]

    return list


def new(
    instance_name: str,
    minecraft_version: MinecraftVersionInfo,
    callbacks: ProgressCallbacks,
) -> None:
    print(f"Creating instance {instance_name}")

    instance_dir = path.join(__INSTANCES_DIR__, instance_name)
    makedirs(instance_dir)
    instance_info = InstanceInfo(minecraft_version=minecraft_version.id)
    _write_info(instance_name, instance_info)
    install_version(minecraft_version, callbacks)

    print("Done")


def _write_info(instance_name: str, instance_info: InstanceInfo) -> None:
    with open(path.join(__INSTANCES_DIR__, instance_name, "instance.toml"), "wb") as f:
        tomli_w.dump(instance_info.dict(), f)


def read_info(instance_name: str) -> InstanceInfo:
    with open(path.join(__INSTANCES_DIR__, instance_name, "instance.toml"), "rb") as f:
        info = InstanceInfo.parse_obj(tomli.load(f))

    # Writes the document file in case it is outdated.
    _write_info(instance_name, info)

    return info


def rename(old_name: str, new_name: str) -> None:
    old_dir = path.join(__INSTANCES_DIR__, old_name)
    new_dir = path.join(__INSTANCES_DIR__, new_name)
    mv(old_dir, new_dir)


def delete(instance_name: str) -> None:
    instance_dir = path.join(__INSTANCES_DIR__, instance_name)
    rmtree(instance_dir)
