# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import json
import subprocess
from enum import Enum
from importlib.metadata import version
from os import listdir, makedirs, path
from os import rename as mv
from shutil import rmtree
from threading import Thread
from typing import Any, List, TypedDict, cast

import tomli
import tomli_w
from minecraft_launcher_lib.command import get_minecraft_command
from minecraft_launcher_lib.install import install_minecraft_version
from minecraft_launcher_lib.runtime import get_executable_path
from minecraft_launcher_lib.types import CallbackDict, MinecraftOptions

from . import accounts, config, dirs

__instances_dir__: str = path.join(dirs.user_data_dir, "instances")


class InstanceType(str, Enum):
    VANILLA = "vanilla"
    FABRIC = "fabric"
    FORGE = "forge"


class InstanceInfo(TypedDict):
    config_version: int
    instance_type: InstanceType
    minecraft_version: str


def list() -> List[str]:
    # check if instances folder exists
    if not path.exists(__instances_dir__):
        makedirs(__instances_dir__)

    list = listdir(__instances_dir__)
    if ".DS_Store" in list:
        list.remove(".DS_Store")

    return list


def _default_instance_info() -> InstanceInfo:
    return {
        "config_version": 1,
        "instance_type": InstanceType.VANILLA,
        "minecraft_version": "",
    }


def new(instance_name: str, minecraft_version: str, callback: CallbackDict) -> None:
    print(f"Creating instance {instance_name}")
    instance_dir = path.join(__instances_dir__, instance_name)
    makedirs(instance_dir)
    instance_info = _default_instance_info()
    instance_info["minecraft_version"] = minecraft_version
    write_info(instance_name, instance_info)
    install_minecraft_version(minecraft_version, dirs.user_data_dir, callback)
    print("Done")


def write_info(instance_name: str, instance_info: InstanceInfo) -> None:
    with open(path.join(__instances_dir__, instance_name, "instance.toml"), "wb") as f:
        tomli_w.dump(cast(dict[str, Any], instance_info), f)


def get_info(instance_name: str) -> InstanceInfo:
    with open(path.join(__instances_dir__, instance_name, "instance.toml"), "rb") as f:
        info = cast(InstanceInfo, tomli.load(f))

    # Update old config with new values
    for key, value in _default_instance_info().items():
        if key not in info:
            info[key] = value

    write_info(instance_name, info)
    return info


def rename(old_name: str, new_name: str) -> None:
    old_dir = path.join(__instances_dir__, old_name)
    new_dir = path.join(__instances_dir__, new_name)
    mv(old_dir, new_dir)


def delete(instance_name: str) -> None:
    instance_dir = path.join(__instances_dir__, instance_name)
    rmtree(instance_dir)


def launch(instance_name: str, account_id: str, callback_function: Any) -> None:
    conf = config.read()

    print("Refreshing account")
    account = accounts.refresh_account(account_id)
    print("Account successfully refreshed")

    instance_info = get_info(instance_name)

    with open(
        path.join(
            dirs.user_data_dir,
            "versions",
            instance_info["minecraft_version"],
            f"{instance_info['minecraft_version']}.json",
        ),
        "r",
    ) as f:
        version_json: dict = json.load(f)

    jvm_version = version_json["javaVersion"]["component"]
    java_executable = get_executable_path(jvm_version, dirs.user_data_dir)
    if java_executable is None:
        java_executable = "java"

    options: MinecraftOptions = {
        "username": account["name"],
        "uuid": account_id,
        "token": account["access_token"],
        "executablePath": java_executable,
        "jvmArguments": [f"-Xmx{conf['jvm_memory']}", f"-Xms{conf['jvm_memory']}"]
        + conf["jvm_options"],
        "launcherName": "Ice Launcher",
        "launcherVersion": version("ice_launcher"),
        "gameDirectory": path.join(__instances_dir__, instance_name),
    }

    minecraft_command = get_minecraft_command(
        instance_info["minecraft_version"], dirs.user_data_dir, options
    )

    def start():
        p = subprocess.Popen(minecraft_command, stdout=subprocess.PIPE)
        callback_function(p)

    Thread(target=start).start()
