# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only


from os import makedirs, path

import httpx
from appdirs import AppDirs

import ice_launcher

__client_id__ = "0018ddff-bd2f-4cc6-b220-66f6a4462a5c"


dirs: AppDirs = AppDirs("ice-launcher", "mq1.eu")
if not path.exists(dirs.user_data_dir):
    makedirs(dirs.user_data_dir)


headers = {
    "user-agent": f"ice-launcher/{ice_launcher.__version__}",
}
http_client = httpx.Client(headers=headers)
