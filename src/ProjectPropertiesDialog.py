# -*- coding: utf-8 -*-

import gi

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gtk
from Utils import DialogSelectScrivener


@Gtk.Template(filename='./ProjectPropertiesDialog.ui')
class ProjectPropertiesDialog(Gtk.Dialog):
    __gtype_name__ = 'ProjectPropertiesDialog'

    propertiesProject = {}

    txtTitle = Gtk.Template.Child(name='txtTitle')
    txtAuthor = Gtk.Template.Child(name='txtAuthor')
    txtSurname = Gtk.Template.Child(name='txtSurname')
    txtForename = Gtk.Template.Child(name='txtForename')
    txtPseudonym = Gtk.Template.Child(name='txtPseudonym')
    txtScrivenerProject = Gtk.Template.Child(name='txtScrivenerProject')
    btnOpenScrivenerProject = Gtk.Template.Child(name='btnOpenScrivenerProject')


    def __init__(self, propriedades):
        super().__init__()
        self.txtTitle.set_text(propriedades.title)
        self.txtAuthor.set_text(propriedades.authorsFullName)
        self.txtSurname.set_text(propriedades.surname)
        self.txtForename.set_text(propriedades.forename)
        self.txtPseudonym.set_text(propriedades.pseudonym)

        self.btnOpenScrivenerProject.connect("clicked", self.on_search_scrivener)

    def properties(self):
        self.propertiesProject['title'] = str(self.txtTitle.get_text().strip())
        self.propertiesProject['authors full name'] = str(self.txtAuthor.get_text().strip())
        self.propertiesProject['surname'] = str(self.txtSurname.get_text().strip())
        self.propertiesProject['forename'] = str(self.txtForename.get_text().strip())
        self.propertiesProject['pseudonym'] = str(self.txtPseudonym.get_text().strip())
        return self.propertiesProject

    def on_search_scrivener(self, button):
        dialogo = DialogSelectScrivener()
        response = dialogo.run()

        if response == Gtk.ResponseType.OK:
            self.txtScrivenerProject.set_text(dialogo.show_file_info())
            dialogo.destroy()

        else:
            dialogo.destroy()


if __name__ == '__main__':
    pass
