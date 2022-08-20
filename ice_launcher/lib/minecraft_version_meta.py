# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import platform
from multiprocessing.pool import AsyncResult, ThreadPool
from os import path

from pydantic import BaseModel, HttpUrl

from . import LIBRARIES_DIR, VERSIONS_DIR, ProgressCallbacks, download_file
from .minecraft_assets import AssetIndex
from .minecraft_libraries import Library, get_valid_artifacts
from .minecraft_rules import Rule


class _ComplexArgument(BaseModel):
    rules: list[Rule]
    value: str | list[str]


class _Arguments(BaseModel):
    game: list[str | _ComplexArgument]


class _Artifact(BaseModel):
    sha1: str
    size: int
    url: HttpUrl


class _Downloads(BaseModel):
    client: _Artifact


class _JavaVersion(BaseModel):
    component: str


class MinecraftVersionMeta(BaseModel):
    arguments: _Arguments
    assetIndex: AssetIndex
    downloads: _Downloads
    javaVersion: _JavaVersion
    libraries: list[Library]
    mainClass: str


def get_version_meta(version_id: str) -> MinecraftVersionMeta:
    version_meta_path = path.join(VERSIONS_DIR, version_id, "meta.json")
    version_meta = MinecraftVersionMeta.parse_file(version_meta_path)

    return version_meta


def install_client(
    version_id: str, artifact: _Artifact, callbacks: ProgressCallbacks, pool: ThreadPool
) -> list[AsyncResult]:
    client_path = path.join(VERSIONS_DIR, version_id, "client.jar")

    result = pool.apply_async(
        download_file,
        (
            artifact.url,
            client_path,
            artifact.sha1,
            callbacks,
        ),
    )

    return [result]


def get_client_path(version_id: str) -> str:
    return path.join(VERSIONS_DIR, version_id, "client.jar")


def get_classpath_string(libraries: list[Library], minecraft_version: str) -> str:
    classpath_separator = ";" if platform.system() == "Windows" else ":"
    artifacts = get_valid_artifacts(libraries)

    jars = [path.join(LIBRARIES_DIR, artifact.path) for artifact in artifacts]
    jars.append(get_client_path(minecraft_version))

    classpath_string = classpath_separator.join(jars)

    return classpath_string
