#!/usr/bin/env python3

# kdbone - A KDB 1.x password manager
# Copyright (C) 2019  Michael Chapman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import copy
import os
import pickle


def config_path(app_name):
    if 'APPDATA' in os.environ:
        config_root = os.environ['APPDATA']
    elif 'XDG_CONFIG_HOME' in os.environ:
        config_root = os.environ['XDG_CONFIG_HOME']
    else:
        config_root = os.path.join(os.environ['HOME'], '.config')
    return os.path.join(config_root, app_name)


class Config:

    def __init__(self, app_name, file_name, default):
        root = config_path(app_name)
        os.makedirs(root, exist_ok=True)
        self.path = os.path.join(root, file_name)
        try:
            with open(self.path, 'rb') as file:
                self.data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.data = copy.deepcopy(default)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __contains__(self, key):
        return key in self.data

    def save(self):
        with open(self.path, 'wb') as file:
            pickle.dump(self.data, file)
