# SPDX-FileCopyrightText: 2022-present Manuel Quarneti <manuelquarneti@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-only

from os import makedirs, path

from appdirs import AppDirs

dirs: AppDirs = AppDirs("ice-launcher", "mq1.eu")
if not path.exists(dirs.user_data_dir):
    makedirs(dirs.user_data_dir)
