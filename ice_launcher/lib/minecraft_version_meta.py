# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from multiprocessing.pool import AsyncResult, ThreadPool
from os import path

from pydantic import BaseModel, HttpUrl

from . import ProgressCallbacks, dirs, download_file
from .minecraft_assets import AssetIndex
from .minecraft_libraries import Library
from .minecraft_rules import Rule

__VERSIONS_PATH__ = path.join(dirs.user_data_dir, "versions")


class _ComplexArgument(BaseModel):
    rules: list[Rule]
    value: str | list[str]


class _Arguments(BaseModel):
    game: list[str] | _ComplexArgument


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
    version_meta_path = path.join(__VERSIONS_PATH__, f"{version_id}.json")
    version_meta = MinecraftVersionMeta.parse_file(version_meta_path)

    return version_meta


def install_client(
    version_id: str, artifact: _Artifact, callbacks: ProgressCallbacks, pool: ThreadPool
) -> list[AsyncResult]:
    client_path = path.join(__VERSIONS_PATH__, f"{version_id}.jar")

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
