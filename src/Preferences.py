# -*- coding: utf-8 -*-

import gi, Utils

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gio, Gtk
from Global import Global
from Utils import AppConfig


@Gtk.Template(filename='Preferences.ui')
class Preferences(Gtk.Dialog):
    __gtype_name__ = 'PreferenceDialog'

    preferences = {}
    settings = Gtk.Settings.get_default()

    # OBJETOS DA TELA
    switch = Gtk.Template.Child(name='darkSwitch')
    check = Gtk.Template.Child(name='chkAutomatically')
    combo = Gtk.Template.Child(name='cmb_update_version')

    def __init__(self):
        super().__init__()
        self.switch.connect('notify::active', self.on_darkSwitch_activate)
        self.check.connect("toggled", self.on_chkAutomatically_toggled)
        appConfig = AppConfig()

        updates = [
            "Releases",
            "Releases and untested version",
        ]
        self.combo.set_entry_text_column(0)
        self.combo.connect("changed", self.on_cmb_update_version_changed)
        for update in updates:
            self.combo.append_text(update)

        darkMode = appConfig.getDarkmode()

        if darkMode == "yes":
            self.preferences['dark mode'] = 'yes'
            self.switch.set_active(True)
        else:
            self.preferences['dark mode'] = 'no'
            self.switch.set_active(False)

        # Update automatically
        updateAutomatically = appConfig.getUpdateAutomatically()
        if updateAutomatically == "yes":
            self.preferences['update automatically'] = 'yes'
            self.check.set_active(True)
        else:
            self.preferences['update automatically'] = 'no'
            self.check.set_active(False)

        # Release
        releases = appConfig.getReleases()
        self.preferences['releases'] = 'yes'

        # # Versões não testadas
        untestedReleases = appConfig.getUntestedReleases()

        if untestedReleases == 'yes':
            self.combo.set_active(1)
            self.preferences['untested releases'] = 'yes'
        else:
            self.combo.set_active(0)
            self.preferences['untested releases'] = 'no'

    # Callbacks
    def on_darkSwitch_activate(self, widget, state):
        if widget.get_active():
            self.preferences.update({'dark mode': 'yes'})
        else:
            self.preferences.update({'dark mode': 'no'})

    def on_chkAutomatically_toggled(self, checkbutton):
        if checkbutton.get_active():
            self.preferences.update({'update automatically': 'yes'})
        else:
            self.preferences.update({'update automatically': 'no'})

    def on_cmb_update_version_changed(self, combobox):
        if self.combo.get_active() == 0:
            self.preferences.update({'releases': 'yes'})
            self.preferences.update({'untested releases': 'no'})
        else:
            self.preferences.update({'releases': 'yes'})
            self.preferences.update({'untested releases': 'yes'})

    def prefs(self):
        return self.preferences


if __name__ == '__main__':
    pass
