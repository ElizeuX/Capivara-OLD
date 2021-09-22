# -*- coding: utf-8 -*-
"""Janela de criação de novo smart group."""

import gi

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gtk


@Gtk.Template(filename='./CapivaraSmartGroup.ui')
class CapivaraSmartGroup(Gtk.Dialog):
    __gtype_name__ = 'CapivaraSmartGroup'

    txtNewSmartGroup = Gtk.Template.Child(name='txtSmartGroupName')
    cboRuleMaster = Gtk.Template.Child(name='cboRuleMaster')
    vBoxRule = Gtk.Template.Child(name='boxRule')


    def __init__(self):
        super().__init__()
        self.set_border_width(10)
        scroller = Gtk.ScrolledWindow()

        self.name_store = Gtk.ListStore(int, str)
        self.name_store.append([1, "name"])
        self.name_store.append([11, "style"])
        self.name_store.append([12, "ethnicity"])
        self.name_store.append([2, "hobbies"])
        self.name_store.append([3, "eye color"])
        self.name_store.append([31, "hair color"])

        self.operator_store = Gtk.ListStore(int, str)
        self.operator_store.append([1, "contains"])
        self.operator_store.append([11, "begins with"])
        self.operator_store.append([12, "end with"])
        self.operator_store.append([2, "is"])
        self.operator_store.append([3, "is not"])

        self.cboRuleMaster.connect("changed", self.on_cboRuleMaster_changed)
        self.cboRuleMaster.set_entry_text_column(0)
        self.cboRuleMaster.append("any", "any")
        self.cboRuleMaster.append("all", "all")

        #self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.vBoxRule)

        hbox = Gtk.Box(spacing=6)
        self.vBoxRule.add(hbox)

        name_combo = Gtk.ComboBox.new_with_model_and_entry(self.name_store)
        name_combo.connect("changed", self.on_name_combo_changed)
        name_combo.set_entry_text_column(1)
        hbox.pack_start(name_combo, False, False, 0)






    def on_cboRuleMaster_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            print("Selected: ID=%d, name=%s" % (row_id, name))
        else:
            entry = combo.get_child()
            print("Entered: %s" % entry.get_text())

    def on_name_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            print("Selected: ID=%d, name=%s" % (row_id, name))
        else:
            entry = combo.get_child()
            print("Entered: %s" % entry.get_text())


    def newSmartGroup(self):
        return str(self.txtNewSmartGroup.get_text())

if __name__ == '__main__':
    pass
