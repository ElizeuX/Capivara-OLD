# -*- coding: utf-8 -*-
#! /usr/bin/env python3

# Make sure the right Gtk version is loaded
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from threading import Thread


class Splash(Thread):
    def __init__(self):
        super(Splash, self).__init__()
        maingrid = Gtk.Grid()
        settings = Gtk.Settings.get_default()

        # Create a popup window
        self.window = Gtk.Window(Gtk.WindowType.POPUP)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect('destroy', Gtk.main_quit)
        self.window.set_default_size(30, 15)

        self.window.add(maingrid)
        image = Gtk.Image()
        #maingrid.set_border_width(1)

        # set the path to the image below
        image.set_from_file(filename='assets/image/Fichacriminal.png')
        maingrid.attach(image, 1, 0, 1, 1)

    def run(self):
        # Show the splash screen without causing startup notification
        # https://developer.gnome.org/gtk3/stable/GtkWindow.html#gtk-window-set-auto-startup-notification
        self.window.set_auto_startup_notification(False)
        self.window.show_all()
        self.window.set_auto_startup_notification(True)

        # Need to call Gtk.main to draw all widgets
        Gtk.main()

    def destroy(self):
        self.window.destroy()
