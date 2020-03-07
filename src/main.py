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


import sys
import tkinter as tk
from tkinter import filedialog

import module.config as cfg


APP_NAME = 'kdbone'

DEFAULT_CONFIG = {
    'width': 480,
    'height': 480
}


def geometry(win, config):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = max(0, (screen_width - config['width']) // 2)
    y = max(0, (screen_height - config['height']) // 2)
    return f"{config['width']}x{config['height']}+{x}+{y}"


class App:

    def __init__(self, title):
        self.root = tk.Tk()
        self.config = cfg.Config(APP_NAME, 'config.pickle', DEFAULT_CONFIG)
        self.root.geometry(geometry(self.root, self.config))
        self.root.title(title)
        self.add_menu_bar()
        self.add_bindings()
        self.root.mainloop()
        self.config.save()

    def add_bindings(self):
        self.root.bind('<Control-q>', self.on_control_q)
        self.root.bind('<Control-o>', self.on_control_o)
        self.root.bind('<Configure>', self.on_configure)

    def add_menu_bar(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label='Open', underline=0,
                              accelerator='Ctrl+O', command=self.open)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', underline=1,
                              accelerator='Ctrl+Q', command=self.quit)
        menu_bar.add_cascade(label='File', underline=0, menu=file_menu)
        self.root.config(menu=menu_bar)

    def on_control_o(self, _):
        self.open()

    def on_control_q(self, _):
        self.quit()

    def on_configure(self, event):
        self.config['width'] = event.width
        self.config['height'] = event.height

    def open(self):
        filename = filedialog.askopenfilename(initialdir='.',
                                              title='Select file',
                                              filetypes=(
                                                  ('kdb files', '*.kdb'),
                                                  ('all files', '*.*')))
        self.parse_file(filename)

    def parse_file(self, filename):
        pass

    def quit(self):
        self.root.destroy()


def main():
    App(APP_NAME)
    return 0


if __name__ == '__main__':
    sys.exit(main())
