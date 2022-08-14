# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from pydantic import BaseModel

from .minecraft_assets import AssetIndex
from .minecraft_libraries import Library


class MinecraftVersionMeta(BaseModel):
    assetIndex: AssetIndex
    libraries: list[Library]
