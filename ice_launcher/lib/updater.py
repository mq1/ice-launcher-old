# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from typing import Optional

import packaging.version
import requests

from ice_launcher import __version__


def _get_latest_release() -> str:
    r = requests.get("https://api.github.com/repos/mq1/ice-launcher/releases/latest")
    return r.json()["tag_name"]


def check_for_updates() -> Optional[str]:
    if "dev" in __version__:
        return None

    current_release = packaging.version.parse(__version__)
    latest_release = packaging.version.parse(_get_latest_release())

    return latest_release.__str__() if latest_release > current_release else None
