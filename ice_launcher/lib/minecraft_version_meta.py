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
    id: str
    libraries: list[Library]


def install_client(
    version_meta: MinecraftVersionMeta, callbacks: ProgressCallbacks
) -> None:
    client_path = path.join(__VERSIONS_PATH__, f"{version_meta.id}.jar")
    download_file(
        url=version_meta.downloads.client.url,
        dest=client_path,
        total_size=version_meta.downloads.client.size,
        sha1hash=version_meta.downloads.client.sha1,
        callbacks=callbacks,
    )
