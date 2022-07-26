# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from typing import List

from minecraft_launcher_lib.types import MinecraftVersionInfo
from minecraft_launcher_lib.utils import get_available_versions

from . import dirs


def get_available() -> List[MinecraftVersionInfo]:
    return get_available_versions(dirs.user_data_dir)
