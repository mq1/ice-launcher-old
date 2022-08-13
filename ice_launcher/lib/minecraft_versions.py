# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from enum import Enum

from pydantic import BaseModel

from . import http_client

__VERSION_MANIFEST_URL__ = (
    "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
)


class _TypeEnum(str, Enum):
    release = "release"
    snapshot = "snapshot"
    old_beta = "old_beta"
    old_alpha = "old_alpha"


class MinecraftVersionInfo(BaseModel):
    id: str
    type: _TypeEnum


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
