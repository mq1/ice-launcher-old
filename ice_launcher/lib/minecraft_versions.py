# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from enum import Enum
from os import path

from pydantic import BaseModel, HttpUrl

from . import ProgressCallbacks, dirs, download_file, http_client
from .minecraft_assets import install_assets
from .minecraft_libraries import install_libraries
from .minecraft_version_meta import MinecraftVersionMeta

__VERSION_MANIFEST_URL__ = (
    "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
)

__VERSIONS_PATH__ = path.join(dirs.user_data_dir, "versions")


class _TypeEnum(str, Enum):
    release = "release"
    snapshot = "snapshot"
    old_beta = "old_beta"
    old_alpha = "old_alpha"


class MinecraftVersionInfo(BaseModel):
    id: str
    type: _TypeEnum
    url: HttpUrl
    sha1: str


class LatestVersions(BaseModel):
    release: str
    snapshot: str


class MinecraftVersionManifest(BaseModel):
    latest: LatestVersions
    versions: list[MinecraftVersionInfo]


def fetch_manifest() -> MinecraftVersionManifest:
    response = http_client.get(__VERSION_MANIFEST_URL__)
    manifest = MinecraftVersionManifest.parse_raw(response.content)

    return manifest


def install_version(
    minecraft_version: MinecraftVersionInfo, callbacks: ProgressCallbacks
) -> None:
    version_meta_path = path.join(__VERSIONS_PATH__, f"{minecraft_version.id}.json")
    download_file(
        url=minecraft_version.url,
        dest=version_meta_path,
        total_size=None,
        sha1hash=minecraft_version.sha1,
        callbacks=None,
    )

    version_meta = MinecraftVersionMeta.parse_file(version_meta_path)

    assets_total_size = version_meta.assetIndex.size + version_meta.assetIndex.totalSize
    libraries_total_size = sum(
        library.downloads.artifact.size for library in version_meta.libraries
    )
    callbacks.set_max(assets_total_size + libraries_total_size)

    callbacks.set_status("Installing assets")
    install_assets(version_meta.assetIndex, callbacks)

    callbacks.set_status("Installing libraries")
    install_libraries(version_meta.libraries, callbacks)
