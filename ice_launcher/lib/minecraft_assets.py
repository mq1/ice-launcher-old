# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from os import path

from pydantic import BaseModel, HttpUrl

from . import ProgressCallbacks, __version__, dirs, download_file

__ASSETS_BASE_URL__ = "https://resources.download.minecraft.net"
__ASSETS_DIR__: str = path.join(dirs.user_data_dir, "assets")


class _ObjectInfo(BaseModel):
    hash: str
    size: int


class _Assets(BaseModel):
    objects: dict[str, _ObjectInfo]


class AssetIndex(BaseModel):
    id: str
    sha1: str
    size: int
    totalSize: int
    url: HttpUrl


def install_assets(asset_index: AssetIndex, callbacks: ProgressCallbacks) -> None:
    asset_index_path = path.join(__ASSETS_DIR__, "indexes", f"{asset_index.id}.json")
    download_file(
        url=asset_index.url,
        dest=asset_index_path,
        total_size=asset_index.size,
        sha1hash=asset_index.sha1,
        callbacks=callbacks,
    )
    assets = _Assets.parse_file(asset_index_path)

    for _, asset_info in assets.objects.items():
        asset_path = path.join(
            __ASSETS_DIR__, "objects", asset_info.hash[:2], asset_info.hash
        )
        asset_url = f"{__ASSETS_BASE_URL__}/{asset_info.hash[:2]}/{asset_info.hash}"
        download_file(
            url=asset_url,
            dest=asset_path,
            total_size=asset_info.size,
            sha1hash=asset_info.hash,
            callbacks=callbacks,
        )
