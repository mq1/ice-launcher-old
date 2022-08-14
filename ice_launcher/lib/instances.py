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
from minecraft_launcher_lib.command import get_minecraft_command
from minecraft_launcher_lib.install import install_minecraft_version
from minecraft_launcher_lib.runtime import get_executable_path
from minecraft_launcher_lib.types import CallbackDict, MinecraftOptions
from pydantic import BaseModel

from . import __version__, accounts, dirs, launcher_config

__instances_dir__: str = path.join(dirs.user_data_dir, "instances")


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
    if not path.exists(__instances_dir__):
        makedirs(__instances_dir__)

    list = [
        x
        for x in listdir(__instances_dir__)
        if path.isdir(path.join(__instances_dir__, x))
    ]

    return list


def new(instance_name: str, minecraft_version: str, callback: CallbackDict) -> None:
    print(f"Creating instance {instance_name}")
    instance_dir = path.join(__instances_dir__, instance_name)
    makedirs(instance_dir)
    instance_info = InstanceInfo(minecraft_version=minecraft_version)
    _write_info(instance_name, instance_info)
    install_minecraft_version(minecraft_version, dirs.user_data_dir, callback)
    print("Done")


def _write_info(instance_name: str, instance_info: InstanceInfo) -> None:
    with open(path.join(__instances_dir__, instance_name, "instance.toml"), "wb") as f:
        tomli_w.dump(instance_info.dict(), f)


def read_info(instance_name: str) -> InstanceInfo:
    with open(path.join(__instances_dir__, instance_name, "instance.toml"), "rb") as f:
        info = InstanceInfo.parse_obj(tomli.load(f))

    # Writes the document file in case it is outdated.
    _write_info(instance_name, info)

    return info


def rename(old_name: str, new_name: str) -> None:
    old_dir = path.join(__instances_dir__, old_name)
    new_dir = path.join(__instances_dir__, new_name)
    mv(old_dir, new_dir)


def delete(instance_name: str) -> None:
    instance_dir = path.join(__instances_dir__, instance_name)
    rmtree(instance_dir)


def launch(instance_name: str, account_id: str, callback_function: Any) -> None:
    config = launcher_config.read()

    print("Refreshing account")
    account = accounts.refresh_account(account_id)
    print("Account successfully refreshed")

    instance_info = read_info(instance_name)

    with open(
        path.join(
            dirs.user_data_dir,
            "versions",
            instance_info.minecraft_version,
            f"{instance_info.minecraft_version}.json",
        ),
        "r",
    ) as f:
        version_json: dict = json.load(f)

    jvm_version = version_json["javaVersion"]["component"]
    java_executable = get_executable_path(jvm_version, dirs.user_data_dir)
    if java_executable is None:
        java_executable = "java"

    options: MinecraftOptions = {
        "username": account.minecraft_username,
        "uuid": account_id,
        "token": account.minecraft_access_token,
        "executablePath": java_executable,
        "jvmArguments": [f"-Xmx{config.jvm_memory}", f"-Xms{config.jvm_memory}"]
        + config.jvm_arguments,
        "launcherName": "Ice Launcher",
        "launcherVersion": __version__,
        "gameDirectory": path.join(__instances_dir__, instance_name),
    }

    minecraft_command = get_minecraft_command(
        instance_info.minecraft_version, dirs.user_data_dir, options
    )

    def start():
        p = subprocess.Popen(minecraft_command, stdout=subprocess.PIPE)
        callback_function(p)

    Thread(target=start).start()
