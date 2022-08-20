# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from typing import Optional

import httpx
import packaging.version
from pydantic import BaseModel

from . import __version__, headers

__LATEST_RELEASE_URL__ = "https://api.github.com/repos/mq1/ice-launcher/releases/latest"


class _ReleaseInfo(BaseModel):
    tag_name: str


def _get_latest_release() -> str:
    """Get the latest release of the launcher."""

    response = httpx.get(__LATEST_RELEASE_URL__, headers=headers)
    release_info = _ReleaseInfo.parse_raw(response.content)

    return release_info.tag_name


def check_for_updates() -> Optional[str]:
    """
    Check if there is a new version of the launcher available.
    Returns the version number if there is a new version, None otherwise.
    """

    current_release = packaging.version.parse(__version__)
    latest_release = packaging.version.parse(_get_latest_release())

    return latest_release.__str__() if latest_release > current_release else None
