# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from os import path
from typing import Coroutine

from pydantic import BaseModel, HttpUrl

from . import __VERSIONS_DIR__, ProgressCallbacks, download_file
from .minecraft_assets import AssetIndex
from .minecraft_libraries import Library
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
    version_meta_path = path.join(__VERSIONS_DIR__, f"{version_id}.json")
    version_meta = MinecraftVersionMeta.parse_file(version_meta_path)

    return version_meta


async def install_client(
    version_id: str, artifact: _Artifact, callbacks: ProgressCallbacks
) -> None:
    client_path = path.join(__VERSIONS_DIR__, f"{version_id}.jar")

    await download_file(
        url=artifact.url,
        dest=client_path,
        sha1hash=artifact.sha1,
        callbacks=callbacks,
    )
