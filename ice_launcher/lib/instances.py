# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import platform
from enum import Enum
from os import listdir, makedirs, path
from os import rename as mv
from shutil import rmtree
from subprocess import Popen
from threading import Thread
from typing import Callable

import tomli
import tomli_w
from pydantic import BaseModel

from . import (
    ProgressCallbacks,
    __version__,
    accounts,
    dirs,
    jre_manager,
    minecraft_version_meta,
)
from .minecraft_libraries import get_classpath_string
from .minecraft_rules import is_rule_list_valid
from .minecraft_versions import MinecraftVersionInfo, install_version

__INSTANCES_DIR__: str = path.join(dirs.user_data_dir, "instances")


class InstanceType(str, Enum):
    vanilla = "vanilla"
    fabric = "fabric"
    forge = "forge"


class InstanceInfo(BaseModel):
    config_version: int = 1
    instance_type: InstanceType = InstanceType.vanilla
    minecraft_version: str = ""
    jre_version: str = "latest"


def list() -> list[str]:
    makedirs(__INSTANCES_DIR__, exist_ok=True)

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


def launch(instance_name: str, account_id: str, callback_function: Callable) -> None:
    print(f"Launching instance {instance_name}")

    print("Refreshing account")
    account = accounts.refresh_account(account_id)
    print("Account successfully refreshed")

    instance_info = read_info(instance_name)
    version_meta = minecraft_version_meta.get_version_meta(
        instance_info.minecraft_version
    )

    jre_version = instance_info.jre_version
    if jre_version == "latest":
        jre_version = jre_manager.get_latest_release()

    is_updated, latest_semver = jre_manager.is_updated(jre_version)
    if not is_updated:
        print("Updating JRE")
        jre_manager.update(jre_version)

    java_path = jre_manager.get_java_path(latest_semver)

    game_arguments = []
    for argument in version_meta.arguments.game:
        if isinstance(argument, minecraft_version_meta._ComplexArgument):
            if is_rule_list_valid(argument.rules):
                argument = argument.value
            else:
                argument = None

        if argument:
            match argument:
                case "${auth_player_name}":
                    argument = account.minecraft_username
                case "${version_name}":
                    argument = instance_info.minecraft_version
                case "${game_directory}":
                    argument = path.join(__INSTANCES_DIR__, instance_name)
                case "${assets_root}":
                    argument = path.join(dirs.user_data_dir, "assets")
                case "${assets_index_name}":
                    argument = version_meta.assetIndex.id
                case "${auth_uuid}":
                    argument = account_id
                case "${auth_access_token}":
                    argument = account.minecraft_access_token
                case "${clientid}":
                    argument = f"ice-launcher/{__version__}"
                case "${auth_xuid}":
                    argument = "0"
                case "${user_type}":
                    argument = "mojang"
                case "${version_type}":
                    argument = instance_info.instance_type.value

            game_arguments.append(argument)

    jvm_arguments = []
    if platform.system() == "Darwin":
        jvm_arguments.append("-XstartOnFirstThread")
    elif platform.system() == "Windows":
        jvm_arguments.append(
            "-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump"
        )
        if platform.release() == "10":
            jvm_arguments.append("-Dos.name=Windows 10")
            jvm_arguments.append("-Dos.version=10.0")
    if platform.machine() in ["x86", "i386", "i686"]:
        jvm_arguments.append("-Xss1M")

    jvm_arguments.append(
        "-Djava.library.path=" + path.join(dirs.user_data_dir, "natives")
    )
    jvm_arguments.append("-Dminecraft.launcher.brand=ice-launcher")
    jvm_arguments.append(f"-Dminecraft.launcher.version={__version__}")
    jvm_arguments.append("-cp")
    jvm_arguments.append(get_classpath_string(version_meta.libraries))

    command = [
        java_path,
        *jvm_arguments,
        version_meta.mainClass,
        *game_arguments,
    ]

    def start():
        process = Popen(command, cwd=path.join(__INSTANCES_DIR__, instance_name))
        callback_function(process)

    Thread(target=start).start()
