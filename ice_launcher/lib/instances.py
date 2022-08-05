# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import json
import subprocess
from importlib.metadata import version
from os import listdir, makedirs, path
from typing import List, TypedDict

from minecraft_launcher_lib.command import get_minecraft_command
from minecraft_launcher_lib.install import install_minecraft_version
from minecraft_launcher_lib.runtime import get_executable_path
from minecraft_launcher_lib.types import MinecraftOptions

from . import accounts, dirs

__instances_dir__: str = path.join(dirs.user_data_dir, "instances")


class InstanceJson(TypedDict):
    config_version: int
    minecraft_version: str


def list() -> List[str]:
    # check if instances folder exists
    if not path.exists(__instances_dir__):
        makedirs(__instances_dir__)

    list = listdir(__instances_dir__)
    if ".DS_Store" in list:
        list.remove(".DS_Store")

    return list


def new(instance_name: str, minecraft_version: str) -> None:
    print("Creating instance")
    instance_dir = path.join(__instances_dir__, instance_name)
    makedirs(instance_dir)
    instance_json: InstanceJson = {
        "config_version": 1,
        "minecraft_version": minecraft_version,
    }
    with open(path.join(instance_dir, "instance.json"), "w") as f:
        json.dump(instance_json, f)

    install_minecraft_version(minecraft_version, dirs.user_data_dir)
    print("Done")


def get_info(instance_name: str) -> InstanceJson:
    with open(path.join(__instances_dir__, instance_name, "instance.json"), "r") as f:
        return json.load(f)


def launch(instance_name: str, account_name) -> None:
    account = next(
        a for a in accounts.read_document()["accounts"] if a["name"] == account_name
    )

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
        "jvmArguments": ["-Xmx2G", "-Xms2G"],
        "launcherName": "Ice Launcher",
        "launcherVersion": version("ice-launcher"),
        "gameDirectory": path.join(__instances_dir__, instance_name),
    }

    minecraft_command = get_minecraft_command(
        instance_json["minecraft_version"], dirs.user_data_dir, options
    )
    subprocess.call(minecraft_command)
