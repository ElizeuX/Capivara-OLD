# -*- coding: utf-8 -*-

import gi

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gtk


@Gtk.Template(filename='PluginsManager.ui')
class PluginsManager(Gtk.Dialog):
    __gtype_name__ = 'PluginsManager'

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    pass
