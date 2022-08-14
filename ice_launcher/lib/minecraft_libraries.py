# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import platform
from enum import Enum
from multiprocessing.pool import AsyncResult, ThreadPool
from os import path
from typing import Optional

from pydantic import BaseModel, HttpUrl

from . import ProgressCallbacks, dirs, download_file
from .minecraft_version_meta import MinecraftVersionMeta

__LIBRARIES_DIR__ = path.join(dirs.user_data_dir, "libraries")


class _Artifact(BaseModel):
    path: str
    sha1: str
    size: int
    url: HttpUrl


class _Action(str, Enum):
    allow = "allow"


class _OsName(str, Enum):
    windows = "windows"
    linux = "linux"
    osx = "osx"


class _Os(BaseModel):
    name: _OsName


class _Rule(BaseModel):
    action: _Action
    os: _Os


class _Downloads(BaseModel):
    artifact: _Artifact
    rules: Optional[list[_Rule]]


class Library(BaseModel):
    downloads: _Downloads


def get_natives_string() -> str:
    """
    Returns the natives string for the current system
    """
    match platform.system():
        case "Linux":
            return "natives-linux"
        case "Darwin":
            match platform.machine():
                case "x86_64":
                    return "natives-macos"
                case "arm64":
                    return "natives-macos-arm64"
        case "Windows":
            match platform.machine():
                case "AMD64":
                    return "natives-windows"
                case "x86":
                    return "natives-windows-x86"

    raise Exception("Unsupported platform")


def is_rule_list_valid(rules: list[_Rule]) -> bool:
    os_name = platform.system().lower().replace("darwin", "osx")

    for rule in rules:
        if rule.action == _Action.allow and rule.os.name == os_name:
            return True

    return False


def install_libraries(
    version_meta: MinecraftVersionMeta, callbacks: ProgressCallbacks
) -> None:
    natives_string = get_natives_string()
    thread_pool = ThreadPool()
    results: list[AsyncResult] = []

    for library in version_meta.libraries:
        library_path = path.join(__LIBRARIES_DIR__, library.downloads.artifact.path)

        if library.downloads.rules and not is_rule_list_valid(library.downloads.rules):
            continue

        if "natives" in library.downloads.artifact.path:
            if natives_string not in library.downloads.artifact.path:
                continue

        if (
            "x86_64" in library.downloads.artifact.path
            and platform.machine() != "x86_64"
        ):
            continue
        if (
            "aarch_64" in library.downloads.artifact.path
            and platform.machine() != "aarch64"
        ):
            continue

        result = thread_pool.apply_async(
            download_file,
            (
                library.downloads.artifact.url,
                library_path,
                library.downloads.artifact.size,
                library.downloads.artifact.sha1,
                callbacks,
            ),
        )
        results.append(result)

    for result in results:
        result.wait()
