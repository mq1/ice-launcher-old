# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from multiprocessing.pool import AsyncResult, ThreadPool
from os import makedirs, path
from pathlib import Path
from typing import Final

from pydantic import BaseModel, HttpUrl

from . import ProgressCallbacks, __version__, dirs, download_file

ASSETS_DOWNLOAD_ENDPOINT: Final[str] = "https://resources.download.minecraft.net"
ASSETS_DIR: Final[str] = path.join(dirs.user_data_dir, "assets")


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


def get_total_assets_size(asset_index: AssetIndex) -> int:
    return asset_index.size + asset_index.totalSize


def install_assets(
    asset_index: AssetIndex, callbacks: ProgressCallbacks, pool: ThreadPool
) -> list[AsyncResult]:
    makedirs(ASSETS_DIR, exist_ok=True)
    makedirs(path.join(ASSETS_DIR, "indexes"), exist_ok=True)
    makedirs(path.join(ASSETS_DIR, "objects"), exist_ok=True)

    asset_index_path = path.join(ASSETS_DIR, "indexes", f"{asset_index.id}.json")
    download_file(
        url=asset_index.url,
        dest=asset_index_path,
        sha1hash=asset_index.sha1,
        callbacks=callbacks,
    )
    assets = _Assets.parse_file(asset_index_path)

    results = []
    for asset_info in assets.objects.values():
        asset_path = path.join(
            ASSETS_DIR, "objects", asset_info.hash[:2], asset_info.hash
        )
        asset_url = (
            f"{ASSETS_DOWNLOAD_ENDPOINT}/{asset_info.hash[:2]}/{asset_info.hash}"
        )

        parent_dir = Path(asset_path).parent.absolute()
        makedirs(parent_dir, exist_ok=True)

        result = pool.apply_async(
            download_file,
            (
                asset_url,
                asset_path,
                asset_info.hash,
                callbacks,
            ),
        )
        results.append(result)

    return results
