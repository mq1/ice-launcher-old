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


class MinecraftVersionMeta(BaseModel):
    assetIndex: AssetIndex
    downloads: _Downloads
    libraries: list[Library]


def install_client(
    version_id: str, client: _Artifact, callbacks: ProgressCallbacks
) -> None:
    client_path = path.join(__VERSIONS_PATH__, f"{version_id}.jar")
    download_file(
        url=client.url,
        dest=client_path,
        total_size=client.size,
        sha1hash=client.sha1,
        callbacks=callbacks,
    )
