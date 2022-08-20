# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from .about import About
from .accounts import Accounts
from .edit_instance import EditInstance
from .instances import Instances
from .logs import Logs
from .new_instance import NewInstance
from .news import News
from .settings import Settings
from .update import Update

__all__ = [
    "About",
    "Accounts",
    "EditInstance",
    "Instances",
    "Logs",
    "NewInstance",
    "News",
    "Settings",
    "Update",
]
