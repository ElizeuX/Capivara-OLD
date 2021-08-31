# -*- coding: utf-8 -*-
"""Janela de criação de novo smart group."""

import gi

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gtk


@Gtk.Template(filename='./CapivaraSmartGroup.ui')
class CapivaraSmartGroup(Gtk.Dialog):
    __gtype_name__ = 'CapivaraSmartGroup'

    txtNewSmartGroup = Gtk.Template.Child(name='txtSmartGroupName')

    def __init__(self):
        super().__init__()

    def newSmartGroup(self):
        return str(self.txtNewSmartGroup.get_text())

if __name__ == '__main__':
    pass
