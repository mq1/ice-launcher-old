# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import platform
from os import listdir, makedirs, path, remove
from shutil import rmtree, unpack_archive

import httpx
from packaging import version
from pydantic import BaseModel, HttpUrl

from . import dirs, download_file, headers

__ENDPOINT__ = "https://api.adoptium.net"
__JRE_DIR__ = path.join(dirs.user_data_dir, "jre")


class _Package(BaseModel):
    checksum: str
    link: HttpUrl
    name: str
    size: int


class _Version(BaseModel):
    semver: str


class _Binary(BaseModel):
    package: _Package


class _Assets(BaseModel):
    binary: _Binary
    version: _Version


def fetch_latest_java_version() -> str:
    path = "/v3/info/available_releases"
    response = httpx.get(f"{__ENDPOINT__}{path}", headers=headers)
    latest_release = response.json()["most_recent_feature_release"]

    return latest_release


def _get_architecture() -> str:
    if platform.machine() in ["AMD64", "x86_64"]:
        return "x64"
    if platform.machine() in ["i386", "i686", "x86"]:
        return "x86"
    if platform.machine() in ["aarch64", "arm64"]:
        return "aarch64"

    raise Exception("Unsupported architecture")


def _get_os() -> str:
    if platform.system() == "Linux":
        return "linux"
    if platform.system() == "Windows":
        return "windows"
    if platform.system() == "Darwin":
        return "mac"

    raise Exception("Unsupported OS")


def _get_assets_info(java_version: str) -> _Assets:
    url_path = f"/v3/assets/latest/{java_version}/hotspot"
    params = {
        "architecture": _get_architecture(),
        "image_type": "jre",
        "os": _get_os(),
        "vendor": "eclipse",
    }

    response = httpx.get(
        f"{__ENDPOINT__}{url_path}",
        headers=headers | {"Accept": "application/json"},
        params=params,
    )
    assets_info_list = response.json()

    return _Assets.parse_obj(assets_info_list[0])


def is_updated(java_version: str) -> bool:
    makedirs(__JRE_DIR__, exist_ok=True)

    assets_info = _get_assets_info(java_version)

    current_semver = [
        dir for dir in listdir(__JRE_DIR__) if path.isdir(path.join(__JRE_DIR__, dir))
    ]
    if len(current_semver) == 0:
        return False

    current_semver = version.parse(
        current_semver[0].replace("jdk-", "").replace("-jre", "")
    )
    latest_semver = version.parse(assets_info.version.semver)

    return current_semver >= latest_semver


def update(java_version: str) -> None:
    makedirs(__JRE_DIR__, exist_ok=True)

    # To be deleted
    previous_files = listdir(__JRE_DIR__)

    assets_info = _get_assets_info(java_version)
    download_url = assets_info.binary.package.link

    extension = "zip" if platform.system() == "Windows" else "tar.gz"
    download_path = path.join(__JRE_DIR__, f"{assets_info.version.semver}.{extension}")

    download_file(
        url=download_url,
        dest=download_path,
    )

    unpack_archive(download_path, __JRE_DIR__)
    remove(download_path)

    # Delete previous files
    for file in previous_files:
        file_path = path.join(__JRE_DIR__, file)
        if path.isdir(file_path):
            rmtree(file_path)

        if path.isfile(file_path):
            remove(file_path)


def get_java_path(version: str) -> str:
    makedirs(__JRE_DIR__, exist_ok=True)

    available_jres = [
        dir for dir in listdir(__JRE_DIR__) if path.isdir(path.join(__JRE_DIR__, dir))
    ]

    current_jre = [dir for dir in available_jres if dir.startswith(f"jdk-{version}")][0]

    if platform.system() == "Windows":
        return path.join("jre", current_jre, "bin", "java.exe")
    if platform.system() == "Darwin":
        return path.join("jre", current_jre, "Contents", "Home", "bin", "java")
    if platform.system() == "Linux":
        return path.join("jre", current_jre, "bin", "java")

    raise Exception("JRE not found")
