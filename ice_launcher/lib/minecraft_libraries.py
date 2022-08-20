# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import platform
from multiprocessing.pool import AsyncResult, ThreadPool
from os import makedirs, path
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, HttpUrl

from . import __VERSIONS_DIR__, ProgressCallbacks, dirs, download_file
from .minecraft_rules import Rule, is_rule_list_valid

__LIBRARIES_DIR__ = path.join(dirs.user_data_dir, "libraries")


class _Artifact(BaseModel):
    path: str
    sha1: str
    size: int
    url: HttpUrl


class _Downloads(BaseModel):
    artifact: _Artifact
    rules: Optional[list[Rule]]


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

    results = []
    for artifact in artifacts:
        library_path = path.join(__LIBRARIES_DIR__, artifact.path)
        parent_dir = Path(library_path).parent.absolute()
        makedirs(parent_dir, exist_ok=True)

        result = pool.apply_async(
            download_file,
            (
                artifact.url,
                library_path,
                artifact.sha1,
                callbacks,
            ),
        )
        results.append(result)

    return results


def get_classpath_string(libraries: list[Library], minecraft_version: str) -> str:
    classpath_separator = ";" if platform.system() == "Windows" else ":"
    artifacts = _get_valid_artifacts(libraries)

    jars = [path.join("libraries", artifact.path) for artifact in artifacts]

    jars.append(path.join("versions", f"{minecraft_version}.jar"))

    classpath_string = classpath_separator.join(jars)

    return classpath_string
