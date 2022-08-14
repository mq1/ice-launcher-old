# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from os import path

from pydantic import BaseModel

from . import ProgressCallbacks, dirs, download_file
from .minecraft_assets import AssetIndex, install_assets
from .minecraft_libraries import Library, install_libraries
from .minecraft_versions import MinecraftVersionInfo

__VERSIONS_PATH__ = path.join(dirs.user_data_dir, "versions")


class MinecraftVersionMeta(BaseModel):
    assetIndex: AssetIndex
    libraries: list[Library]


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
