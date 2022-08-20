# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only


import hashlib
import lzma
import os
import stat
from os import chmod, makedirs, path, remove
from typing import Callable, Optional, TypedDict

import httpx
from appdirs import AppDirs
from pydantic import BaseModel

dirs: AppDirs = AppDirs("ice-launcher", "mq1.eu")
makedirs(dirs.user_data_dir, exist_ok=True)


__version__ = "0.0.16"
__CLIENT_ID__ = "0018ddff-bd2f-4cc6-b220-66f6a4462a5c"
__VERSIONS_DIR__ = path.join(dirs.user_data_dir, "versions")


headers = {
    "user-agent": f"ice-launcher/{__version__}",
}
http_client = httpx.Client(headers=headers, follow_redirects=True)


class ProgressCallbacks(BaseModel):
    set_max: Callable[[int], None]
    increment_value_by: Callable[[int], None]
    set_status: Callable[[str], None]
    reset: Callable[[], None]


async def download_file(
    url: str,
    dest: str,
    sha1hash: Optional[str] = None,
    callbacks: Optional[ProgressCallbacks] = None,
    is_lzma: bool = False,
    set_executable: bool = False,
) -> None:
    # If the file already exists, we check if the hash matches.
    if path.exists(dest):
        print(f"File {dest} already exists, checking hash...")

        if sha1hash:
            sha1 = hashlib.sha1()

            with open(dest, "rb") as f:
                while chunk := f.read(65536):  # Read 64kb chunks.
                    sha1.update(chunk)

            if sha1.hexdigest() == sha1hash:
                if callbacks:
                    file_size = path.getsize(dest)
                    callbacks.increment_value_by(file_size)
                
                print(f"{dest} Hash matches, skipping download.")
                return

        remove(dest)

    print("Downloading file from", url, "to", dest)

    with open(dest, "wb") as file:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()

                async for chunk in response.aiter_bytes(65536):  # Read 64kb chunks.
                    if callbacks:
                        callbacks.increment_value_by(len(chunk))

                    if is_lzma:
                        chunk = lzma.decompress(chunk)

                    file.write(chunk)

    print(f"Downloaded {dest}")

    if set_executable:
        st = os.stat(dest)
        chmod(dest, st.st_mode | stat.S_IEXEC)
