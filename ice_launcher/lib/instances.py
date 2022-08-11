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
from typing import List, TypedDict

from minecraft_launcher_lib.command import get_minecraft_command
from minecraft_launcher_lib.install import install_minecraft_version
from minecraft_launcher_lib.microsoft_account import complete_refresh
from minecraft_launcher_lib.runtime import get_executable_path
from minecraft_launcher_lib.types import MinecraftOptions, CallbackDict

from ice_launcher import __client_id__

from . import accounts, config, dirs

__instances_dir__: str = path.join(dirs.user_data_dir, "instances")


class InstanceType(str, Enum):
    VANILLA = "vanilla"
    FABRIC = "fabric"
    FORGE = "forge"


class InstanceJson(TypedDict):
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


def _default_instance_json() -> InstanceJson:
    return {
        "config_version": 1,
        "instance_type": InstanceType.VANILLA,
        "minecraft_version": "",
    }


def new(instance_name: str, minecraft_version: str, callback: CallbackDict) -> None:
    print("Creating instance")
    instance_dir = path.join(__instances_dir__, instance_name)
    makedirs(instance_dir)
    instance_json = _default_instance_json()
    instance_json["minecraft_version"] = minecraft_version
    with open(path.join(instance_dir, "instance.json"), "w") as f:
        json.dump(instance_json, f)

    install_minecraft_version(minecraft_version, dirs.user_data_dir, callback)
    print("Done")


def write_info(instance_name: str, instance_json: InstanceJson) -> None:
    with open(path.join(__instances_dir__, instance_name, "instance.json"), "w") as f:
        json.dump(instance_json, f)


def get_info(instance_name: str) -> InstanceJson:
    with open(path.join(__instances_dir__, instance_name, "instance.json"), "r") as f:
        info = json.load(f)

    # Update old config with new values
    for key, value in _default_instance_json().items():
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


def launch(instance_name: str, account_name: str) -> None:
    conf = config.read()
    account_document = accounts.read_document()

    account = None
    for i in range(len(account_document["accounts"])):
        if account_document["accounts"][i]["name"] == account_name:
            account = account_document["accounts"][i]
            print("Refreshing account")
            account = complete_refresh(
                client_id=__client_id__,
                client_secret=None,
                redirect_uri=None,
                refresh_token=account["refresh_token"],
            )
            account_document["accounts"][i] = account
            accounts.write_document(account_document)
            print("Account successfully refreshed")
            break

    assert account is not None

    instance_dir = path.join(__instances_dir__, instance_name)
    with open(path.join(instance_dir, "instance.json"), "r") as f:
        instance_json: InstanceJson = json.load(f)

    with open(
        path.join(
            dirs.user_data_dir,
            "versions",
            instance_json["minecraft_version"],
            f"{instance_json['minecraft_version']}.json",
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
        "uuid": account["id"],
        "token": account["access_token"],
        "executablePath": java_executable,
        "jvmArguments": [f"-Xmx{conf['jvm_memory']}", f"-Xms{conf['jvm_memory']}"]
        + conf["jvm_options"],
        "launcherName": "Ice Launcher",
        "launcherVersion": version("ice_launcher"),
        "gameDirectory": path.join(__instances_dir__, instance_name),
    }

    minecraft_command = get_minecraft_command(
        instance_json["minecraft_version"], dirs.user_data_dir, options
    )
    subprocess.call(minecraft_command)
