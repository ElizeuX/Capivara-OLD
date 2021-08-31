# -*- coding: utf-8 -*-

import gi

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gtk


@Gtk.Template(filename='./NewGroupDialog.ui')
class NewGroupDialog(Gtk.Dialog):
    __gtype_name__ = 'NewGroupDialog'
    txtNewGroup= Gtk.Template.Child(name='txtGroup')

    def __init__(self):
        super().__init__()

    def newGroup(self):
        return str(self.txtNewGroup.get_text())

if __name__ == '__main__':
    pass
