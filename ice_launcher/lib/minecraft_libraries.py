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


def get_total_libraries_size(libraries: list[Library]) -> int:
    return sum(library.downloads.artifact.size for library in libraries)


def _get_valid_artifacts(libraries: list[Library]) -> list[_Artifact]:
    natives_string = get_natives_string()

    valid_artifacts = []
    for library in libraries:
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

        valid_artifacts.append(library.downloads.artifact)

    return valid_artifacts


def install_libraries(
    libraries: list[Library], callbacks: ProgressCallbacks, pool: ThreadPool
) -> list[AsyncResult]:
    artifacts = _get_valid_artifacts(libraries)

    results: list[AsyncResult] = []
    for artifact in artifacts:
        library_path = path.join(__LIBRARIES_DIR__, artifact.path)

        result = pool.apply_async(
            download_file,
            (
                artifact.url,
                library_path,
                artifact.size,
                artifact.sha1,
                callbacks,
            ),
        )
        results.append(result)

    return results


def get_classpath_string(libraries: list[Library]) -> str:
    classpath_separator = ";" if platform.system() == "Windows" else ":"
    artifacts = _get_valid_artifacts(libraries)
    classpath_string = classpath_separator.join(
        path.join(__LIBRARIES_DIR__, artifact.path) for artifact in artifacts
    )

    return classpath_string
