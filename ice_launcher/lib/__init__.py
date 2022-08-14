# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only


import hashlib
from os import makedirs, path
from typing import Callable, Optional

import httpx
from appdirs import AppDirs
from pydantic import BaseModel

__version__ = "0.0.16"
__CLIENT_ID__ = "0018ddff-bd2f-4cc6-b220-66f6a4462a5c"


dirs: AppDirs = AppDirs("ice-launcher", "mq1.eu")
if not path.exists(dirs.user_data_dir):
    makedirs(dirs.user_data_dir)


headers = {
    "user-agent": f"ice-launcher/{__version__}",
}
http_client = httpx.Client(headers=headers)


class ProgressCallbacks(BaseModel):
    set_max: Callable[[int], None]
    increment_value_by: Callable[[int], None]
    set_status: Callable[[str], None]


def download_file(
    url: str,
    dest: str,
    total_size: Optional[int],
    sha1hash: str,
    callbacks: Optional[ProgressCallbacks],
) -> None:
    # If the file already exists, we check if the hash matches.
    if path.exists(dest):
        sha1 = hashlib.sha1()

        with open(dest, "rb") as f:
            while True:
                chunk = f.read(65536)  # Read 64kb chunks.
                if not chunk:
                    break
                sha1.update(chunk)

        if sha1.hexdigest() == sha1hash:
            if callbacks and total_size:
                callbacks.increment_value_by(total_size)
            return

    with open(dest, "wb") as file:
        with http_client.stream("GET", url) as response:
            for chunk in response.iter_bytes(65536):  # 64kb
                if callbacks:
                    callbacks.increment_value_by(len(chunk))
                file.write(chunk)
