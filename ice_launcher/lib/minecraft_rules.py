# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

import platform
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class _Action(str, Enum):
    allow = "allow"


class _OsName(str, Enum):
    windows = "windows"
    linux = "linux"
    osx = "osx"


class _Os(BaseModel):
    name: _OsName


class _Feature(str, Enum):
    is_demo_user = "is_demo_user"
    has_custom_resolution = "has_custom_resolution"


class Rule(BaseModel):
    action: _Action
    os: Optional[_Os]
    features: Optional[dict[_Feature, bool]]


def is_rule_list_valid(rules: list[Rule]) -> bool:
    os_name = platform.system().lower().replace("darwin", "osx")

    for rule in rules:
        if rule.features:
            return False
        if rule.os:
            if rule.action == _Action.allow and rule.os.name == os_name:
                return True

    return False
