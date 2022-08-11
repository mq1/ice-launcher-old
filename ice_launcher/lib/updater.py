# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from importlib.metadata import version
from typing import Optional

import packaging.version
import requests


def _get_latest_release() -> str:
    r = requests.get("https://api.github.com/repos/mq1/ice-launcher/releases/latest")
    return r.json()["tag_name"]


def check_for_updates() -> Optional[str]:
    current_version = version("ice_launcher")

    if "dev" in current_version:
        return None

    current_release = packaging.version.parse(current_version)
    latest_release = packaging.version.parse(_get_latest_release())

    return latest_release.__str__() if latest_release > current_release else None
