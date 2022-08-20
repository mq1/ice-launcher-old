# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from enum import Enum
from multiprocessing.pool import ThreadPool
from os import makedirs, path

import httpx
from pydantic import BaseModel, HttpUrl

from . import ProgressCallbacks, dirs, download_file, headers
from .minecraft_assets import get_total_assets_size, install_assets
from .minecraft_libraries import get_total_libraries_size, install_libraries
from .minecraft_version_meta import MinecraftVersionMeta, install_client

__VERSION_MANIFEST_URL__ = (
    "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
)

__VERSION_MANIFESTS_PATH__ = path.join(dirs.user_data_dir, "versions")


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
    response = httpx.get(__VERSION_MANIFEST_URL__, headers=headers)
    manifest = MinecraftVersionManifest.parse_raw(response.content)

    return manifest


def install_version(
    minecraft_version: MinecraftVersionInfo, callbacks: ProgressCallbacks
) -> None:
    makedirs(__VERSION_MANIFESTS_PATH__, exist_ok=True)

    version_meta_path = path.join(
        __VERSION_MANIFESTS_PATH__, f"{minecraft_version.id}.json"
    )
    download_file(
        url=minecraft_version.url,
        dest=version_meta_path,
        sha1hash=minecraft_version.sha1,
    )

    version_meta = MinecraftVersionMeta.parse_file(version_meta_path)

    total_size = (
        get_total_assets_size(version_meta.assetIndex)
        + get_total_libraries_size(version_meta.libraries)
        + version_meta.downloads.client.size
    )
    callbacks.set_status("Downloading required files")
    callbacks.set_max(total_size)

    with ThreadPool() as pool:
        results = install_assets(version_meta.assetIndex, callbacks, pool)
        results += install_libraries(version_meta.libraries, callbacks, pool)
        results += install_client(
            minecraft_version.id, version_meta.downloads.client, callbacks, pool
        )

        for result in results:
            result.wait()
