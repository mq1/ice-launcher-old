# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from typing import List

from .about import About
from .accounts import Accounts
from .instances import Instances
from .news import News
from .settings import Settings
from .update import Update

__all__: List[str] = ["About", "Accounts", "Instances", "News", "Settings", "Update"]
