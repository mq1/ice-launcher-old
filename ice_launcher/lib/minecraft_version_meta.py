# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from os import path

from pydantic import BaseModel, HttpUrl

from . import ProgressCallbacks, dirs, download_file
from .minecraft_assets import AssetIndex
from .minecraft_libraries import Library

__VERSIONS_PATH__ = path.join(dirs.user_data_dir, "versions")


class _Artifact(BaseModel):
    sha1: str
    size: int
    url: HttpUrl


class _Downloads(BaseModel):
    client: _Artifact


class _JavaVersion(BaseModel):
    component: str


class MinecraftVersionMeta(BaseModel):
    assetIndex: AssetIndex
    downloads: _Downloads
    javaVersion: _JavaVersion
    libraries: list[Library]


def install_client(
    version_id: str, artifact: _Artifact, callbacks: ProgressCallbacks
) -> None:
    callbacks.reset()
    callbacks.set_status("Installing client")
    callbacks.set_max(artifact.size)

    client_path = path.join(__VERSIONS_PATH__, f"{version_id}.jar")
    download_file(
        url=artifact.url,
        dest=client_path,
        total_size=artifact.size,
        sha1hash=artifact.sha1,
        callbacks=callbacks,
    )
