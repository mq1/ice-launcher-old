# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import json
import platform
from enum import Enum
from multiprocessing.pool import AsyncResult, ThreadPool
from os import makedirs, path, symlink
from typing import Optional

from pydantic import BaseModel, HttpUrl

from . import ProgressCallbacks, dirs, download_file

__RUNTIME_INDEX_URL__ = "https://piston-meta.mojang.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json"
__RUNTIME_META_DIR__ = path.join(dirs.user_data_dir, "runtimes")
__RUNTIMES_DIR__ = path.join(dirs.user_data_dir, "runtimes")


class RuntimeInfo(BaseModel):
    sha1: str
    size: int
    url: HttpUrl


class _Runtime(BaseModel):
    manifest: RuntimeInfo


class _Download(BaseModel):
    sha1: str
    size: int
    url: HttpUrl


class _Downloads(BaseModel):
    lzma: Optional[_Download]
    raw: _Download


class _FileType(str, Enum):
    file = "file"
    directory = "directory"
    link = "link"


class _File(BaseModel):
    downloads: Optional[_Downloads] = None
    executable: Optional[bool] = None
    target: Optional[str] = None
    type: _FileType


class RuntimeMeta(BaseModel):
    files: dict[str, _File]


def _get_runtime_platform_string() -> str:
    """
    Get the name used the identify the platform
    """
    match platform.system():
        case "Linux":
            match platform.machine():
                case "x86_64":
                    return "linux"
                case "i386" | "i686":
                    return "linux-i386"
        case "Darwin":
            match platform.machine():
                case "x86_64":
                    return "mac-os"
                case "arm64":
                    return "mac-os-arm64"
        case "Windows":
            match platform.machine():
                case "AMD64":
                    return "windows-x64"
                case "x86":
                    return "windows-x86"

    raise Exception("Unsupported platform")


def get_runtime_meta(name: str) -> RuntimeMeta:
    if not path.exists(__RUNTIME_META_DIR__):
        makedirs(__RUNTIME_META_DIR__)

    runtime_index_path = path.join(__RUNTIME_META_DIR__, "index.json")
    download_file(
        url=__RUNTIME_INDEX_URL__,
        dest=runtime_index_path,
        total_size=None,
        sha1hash=None,
        callbacks=None,
    )
    with open(runtime_index_path) as f:
        runtime_index = json.load(f)

    platform_string = _get_runtime_platform_string()

    runtime = _Runtime.parse_obj(runtime_index[platform_string][name][0])
    runtime_meta_path = path.join(__RUNTIMES_DIR__, f"{name}.json")
    download_file(
        url=runtime.manifest.url,
        dest=runtime_meta_path,
        total_size=None,
        sha1hash=runtime.manifest.sha1,
        callbacks=None,
    )
    runtime_meta = RuntimeMeta.parse_file(runtime_meta_path)

    return runtime_meta


def get_total_runtime_size(name: str) -> int:
    runtime_meta = get_runtime_meta(name)

    total_size = 0
    for file_info in runtime_meta.files.values():
        if file_info.type == _FileType.file and file_info.downloads is not None:
            if file_info.downloads.lzma is not None:
                total_size += file_info.downloads.lzma.size
            else:
                total_size += file_info.downloads.raw.size

    return total_size


def install_runtime(
    name: str, callbacks: ProgressCallbacks, pool: ThreadPool
) -> list[AsyncResult]:
    runtime_meta = get_runtime_meta(name)
    runtime_path = path.join(__RUNTIMES_DIR__, name)
    makedirs(runtime_path, exist_ok=True)

    results: list[AsyncResult] = []
    for file_name, file_meta in runtime_meta.files.items():
        match file_meta.type:
            case _FileType.file:
                if file_meta.downloads is not None:
                    if file_meta.downloads.lzma is not None:
                        result = pool.apply_async(
                            download_file,
                            args=(
                                file_meta.downloads.lzma.url,
                                path.join(runtime_path, file_name),
                                file_meta.downloads.lzma.size,
                                file_meta.downloads.lzma.sha1,
                                callbacks,
                                True,
                            ),
                        )
                    else:
                        result = pool.apply_async(
                            download_file,
                            args=(
                                file_meta.downloads.raw.url,
                                path.join(runtime_path, file_name),
                                file_meta.downloads.raw.size,
                                file_meta.downloads.raw.sha1,
                                callbacks,
                                False,
                            ),
                        )
                    results.append(result)
            case _FileType.directory:
                makedirs(path.join(runtime_path, file_name), exist_ok=True)
            case _FileType.link:
                file_path = path.join(runtime_path, file_name)
                if file_meta.target is not None and not path.exists(file_path):
                    symlink(
                        file_meta.target,
                        file_path,
                    )
            case _:
                raise Exception("Unsupported file type")

    return results


def get_executable_path(name: str) -> str:
    runtime_dir = path.join(__RUNTIMES_DIR__, name)

    match platform.system():
        case "Linux":
            return path.join(runtime_dir, "bin", "java")
        case "Darwin":
            return path.join(
                runtime_dir, "jre.bundle", "Contents", "Home", "bin", "java"
            )
        case "Windows":
            return path.join(runtime_dir, "bin", "java.exe")

    raise Exception("Unsupported platform")
