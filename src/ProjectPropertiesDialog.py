# -*- coding: utf-8 -*-

import gi

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gtk
from Utils import DialogSelectScrivener, DialogSelectAeon



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
    txtAeonProject = Gtk.Template.Child(name='txtAeonProject')

    btnOpenScrivenerProject = Gtk.Template.Child(name='btnOpenScrivenerProject')
    btnOpenAeonProject = Gtk.Template.Child(name='btnOpenAeonProject')


    def __init__(self, propriedades):
        super().__init__()
        self.txtTitle.set_text(propriedades.title)
        self.txtAuthor.set_text(propriedades.authorsFullName)
        self.txtSurname.set_text(propriedades.surname)
        self.txtForename.set_text(propriedades.forename)
        self.txtPseudonym.set_text(propriedades.pseudonym)
        self.txtScrivenerProject.set_text(propriedades.scrivener_project)
        self.txtAeonProject.set_text(propriedades.aeon_project)

        self.btnOpenScrivenerProject.connect("clicked", self.on_search_scrivener)
        self.btnOpenAeonProject.connect("clicked", self.on_search_aeon)

    def properties(self):
        self.propertiesProject['title'] = str(self.txtTitle.get_text().strip())
        self.propertiesProject['authors full name'] = str(self.txtAuthor.get_text().strip())
        self.propertiesProject['surname'] = str(self.txtSurname.get_text().strip())
        self.propertiesProject['forename'] = str(self.txtForename.get_text().strip())
        self.propertiesProject['pseudonym'] = str(self.txtPseudonym.get_text().strip())
        self.propertiesProject['scrivener project'] = str(self.txtScrivenerProject.get_text().strip())
        self.propertiesProject['aeon project'] = str(self.txtAeonProject.get_text().strip())
        return self.propertiesProject

    def on_search_scrivener(self, button):
        dialogo = DialogSelectScrivener()
        response = dialogo.run()

        if response == Gtk.ResponseType.OK:
            self.txtScrivenerProject.set_text(dialogo.show_file_info())
            dialogo.destroy()

        else:
            dialogo.destroy()

    def on_search_aeon(self, button):
        dialogo = DialogSelectAeon()
        response = dialogo.run()

        if response == Gtk.ResponseType.OK:
            self.txtAeonProject.set_text(dialogo.show_file_info())
            dialogo.destroy()

        else:
            dialogo.destroy()


if __name__ == '__main__':
    pass
