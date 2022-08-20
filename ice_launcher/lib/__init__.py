# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only


import hashlib
import lzma
import os
import stat
from os import chmod, makedirs, path, remove
from typing import Callable, Final, Optional

import httpx
from appdirs import AppDirs
from pydantic import BaseModel

dirs: AppDirs = AppDirs("ice-launcher", "mq1.eu")
makedirs(dirs.user_data_dir, exist_ok=True)


__version__: Final[str] = "0.0.16"
CLIENT_ID: Final[str] = "0018ddff-bd2f-4cc6-b220-66f6a4462a5c"
VERSIONS_DIR: Final[str] = path.join(dirs.user_data_dir, "versions")
LIBRARIES_DIR: Final[str] = path.join(dirs.user_data_dir, "libraries")


headers = {
    "user-agent": f"ice-launcher/{__version__}",
}


class ProgressCallbacks(BaseModel):
    set_max: Callable[[int], None]
    increment_value_by: Callable[[int], None]
    set_status: Callable[[str], None]
    reset: Callable[[], None]


def download_file(
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

        print(f"{dest} Hash does not match, redownloading.")
        remove(dest)

    print("Downloading file from", url, "to", dest)

    with open(dest, "wb") as file:
        with httpx.stream("GET", url, headers=headers) as response:
            for chunk in response.iter_bytes(65536):  # Read 64kb chunks.
                if callbacks:
                    callbacks.increment_value_by(len(chunk))

                if is_lzma:
                    chunk = lzma.decompress(chunk)

                file.write(chunk)

    print(f"Downloaded {dest}")

    if set_executable:
        st = os.stat(dest)
        chmod(dest, st.st_mode | stat.S_IEXEC)
