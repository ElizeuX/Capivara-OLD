# -*- coding: utf-8 -*-
"""Capivara"""

import gi

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gio, Gtk, GdkPixbuf, GLib

import Global
from Global import Global
from Utils import AppConfig, DialogUpdateAutomatically, DialogSelectFile, DialogSaveFile, JsonTools, Treeview
import PluginsManager
import webbrowser
from CapivaraSmartGroup import CapivaraSmartGroup
from DataAccess import DataUtils, FileInformation, ProjectProperties, Character, Core, SmartGroup

from time import sleep

import logging

logging.basicConfig(level=logging.INFO)

# importar Telas
from Preferences import Preferences
from ProjectPropertiesDialog import ProjectPropertiesDialog
from NewGroupDialog import NewGroupDialog
from PluginsManager import PluginsManager


@Gtk.Template(filename='MainWindow.ui')
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'MainWindow'
    settings = Gtk.Settings.get_default()

    btn_search = Gtk.Template.Child(name='btn_search')
    search_bar = Gtk.Template.Child(name='search_bar')
    statusbar = Gtk.Template.Child(name='statusbar')
    header_bar = Gtk.Template.Child(name='header_bar')
    treeView = Gtk.Template.Child(name='treeview')
    # spinner = Gtk.Template.Child(name='spinner')
    info_bar = Gtk.Template.Child(name='info_bar')
    list_store = Gtk.Template.Child(name='list_store')


    # Obtendo as configurações
    appConfig = AppConfig()

    if appConfig.getDarkmode() == 'yes':
        settings.set_property('gtk-application-prefer-dark-theme', True)
    else:
        settings.set_property('gtk-application-prefer-dark-theme', False)

    logo = GdkPixbuf.Pixbuf.new_from_file(filename='assets/icons/icon.png')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.context_id = self.statusbar.get_context_id(
            context_description='exemplo',
        )

        self.statusbar_show_msg("Teste")

        # NOVA VERSÃO
        # TODO: Verificar se existe nova versão e apresentar no Info
        #if not self.info_bar.get_revealed():
        self.info_bar.set_revealed(revealed=True)
        GLib.timeout_add_seconds(priority=0, interval=5, function=self.info_bar_timeout)

        # CONSTRUINDO O MENU POPOVER DINAMICAMENTE
        popover = Gtk.Template.Child(name='menu-popover')
        # menu_item = Gtk.MenuItem("Excluir Capivara")
        # popover.append(menu_item)
        # menu_item = Gtk.MenuItem("Imprimir Capivara")
        # popover.append(menu_item)

        # ABRE UM PROJETO VAZIO
        propertiesProject = {}
        propertiesProject['title'] = "Untitled"
        propertiesProject['authors full name'] = ""
        propertiesProject['surname'] = ""
        propertiesProject['forename'] = ""
        propertiesProject['pseudonym'] = ""

        dataUtils = DataUtils()
        dataUtils.LoadCapivaraFileEmpty(propertiesProject)

        Biografia_Character = [
            (1965, 'Nascimento'), (1974, 'Evento 1'), (1976, 'Evento 2'), (1979, 'Evento 3'),
            (1980, 'Evento 4'), (1985, 'Evento 5'), (1987, 'Evento 6'),
        ]

        capivara = {
            "character": [
                {
                    "id": 1,
                    "name": "Frodo Baggins 2"
                },
                {
                    "id": 2,
                    "name": "Aragorn (Strider) 2"
                },
                {
                    "id": 3,
                    "name": "Meriadoc (Merry) Brandybuck 2"
                },
                {
                    "id": 4,
                    "name": "Boromir 2"
                }
            ],
            "core": [
                {
                    "id": 1,
                    "description": "The Fellowship of the Ring"
                },
                {
                    "id": 2,
                    "description": "Allies of the Fellowship"
                },
                {
                    "id": 3,
                    "description": "Opponents of the fellowship"
                },
                {
                    "id": 4,
                    "description": "Fellowship"
                },
                {
                    "id": 5,
                    "description": "Ring"
                },
                {
                    "id": 6,
                    "description": "Allies"
                }
            ],
            "smart group": [
                {
                    "id": 1,
                    "description": "Elves"
                },
                {
                    "id": 2,
                    "description": "Hobbits"
                },
                {
                    "id": 3,
                    "description": "Humans"
                },
                {
                    "id": 4,
                    "description": "Female character"
                }
            ]
        }

        for state in Biografia_Character:
            self.list_store.append(row=state)

            self.show_all()

        Treeview(self.treeView, capivara)


    @Gtk.Template.Callback()
    def on_btn_search_clicked(self, widget):
        print("Botão pesquisar acionado")

    @Gtk.Template.Callback()
    def on_btn_open_project_clicked(self, widget):
        dialog = DialogSelectFile(select_multiple=1)
        dialog.set_transient_for(parent=self)

        # Executando a janela de dialogo e aguardando uma resposta.
        response = dialog.run()

        # Verificando a resposta recebida.
        if response == Gtk.ResponseType.OK:
            logging.info("Abrindo arquivo : " + dialog.show_file_info())

            # Carregar Capivara salva
            fileOpen = dialog.show_file_info()
            dataUtils = DataUtils()
            capivara = dataUtils.loadCapivaraFile(fileOpen)

            Treeview(self.treeView, capivara)

            projectProperties = ProjectProperties.get()
            self.header_bar.set_title(projectProperties.title)
            self.header_bar.set_subtitle(projectProperties.surname + ', ' + projectProperties.forename)

        elif response == Gtk.ResponseType.NO:
            pass

        # Destruindo a janela de dialogo.
        dialog.destroy()


    @Gtk.Template.Callback()
    def on_btn_new_project_clicked(self, widget):
        projectProperties = ProjectProperties()
        projectProperties.title = "Untitled"
        projectProperties.authorsFullName = ""
        projectProperties.surname = ""
        projectProperties.forename = ""
        projectProperties.pseudonym = ""

        dialog = ProjectPropertiesDialog(projectProperties)
        dialog.set_transient_for(parent=self)
        response = dialog.run()

        # Verificando qual botão foi pressionado.
        if response == Gtk.ResponseType.YES:
            projectProject = dialog.properties()
            dataUtils = DataUtils()
            dataUtils.LoadCapivaraFileEmpty(projectProject)
            capivara = {'version model': '0.1.0', 'creator': 'Capivara 0.1.0', 'device': 'ELIZEU-PC', 'modified': '2021-08-19 14:08:59.496007', 'project properties': {'title': 'Deixa-me enterrar meu pai', 'abbreviated title': 'Deixa-me enterrar meu pai', 'authors full name': 'Elizeu Xavier', 'surname': 'Xavier', 'forename': 'Elizeu', 'pseudonym': ''}, 'character': [{"name" : "unnamed"}], 'core': [], 'smart group': [], 'tag': []}
            Treeview(self.treeView, capivara)
        elif response == Gtk.ResponseType.NO:
            pass

        dialog.destroy()

    @Gtk.Template.Callback()
    def on_btn_preferences_clicked(self, widget):
        dialog = Preferences()
        dialog.set_transient_for(parent=self)
        response = dialog.run()

        # Verificando qual botão foi pressionado.
        if response == Gtk.ResponseType.YES:
            preferences = dialog.prefs()
            appConfig = AppConfig()
            appConfig.setDarkmode(preferences['dark mode'])
            appConfig.setUpdateAutomatically(preferences['update automatically'])
            appConfig.setReleases(preferences['releases'])
            appConfig.setUntestedReleases(preferences['untested releases'])
            appConfig.serialize()

            # ATUALIZAR O DARK MODE
            if preferences['dark mode'] == 'yes':
                self.settings.set_property('gtk-application-prefer-dark-theme', True)
                Global.set("darkMode", "yes")
            else:
                self.settings.set_property('gtk-application-prefer-dark-theme', False)
                Global.set("darkMode", "no")

        elif response == Gtk.ResponseType.NO:
            pass

        dialog.destroy()

    @Gtk.Template.Callback()
    def on_btn_save_clicked(self, widget):
        dataUtils = DataUtils()
        fileSave = "/Users/Elizeu/OneDrive - PRODESP/Documents/My Capivaras/Teste_Salvar_arquivo.capivara"
        dataUtils.saveCapivaraFile(fileSave)

    # SALVAR COMO
    @Gtk.Template.Callback()
    def on_btn_save_as_clicked(self, widget):
        print("Botão salvar como acionado")
        dialog = DialogSaveFile()
        dialog.set_transient_for(parent=self)

        # Executando a janela de dialogo e aguardando uma resposta.
        response = dialog.run()

        # Verificando a resposta recebida.
        if response == Gtk.ResponseType.OK:
            dataUtils = DataUtils()
            fileSave = dialog.save_file()
            dataUtils.saveCapivaraFile(fileSave)

        # Destruindo a janela de dialogo.
        dialog.destroy()

    @Gtk.Template.Callback()
    def menu_item_clicked(self, widget):
        print(widget.props)

    @Gtk.Template.Callback()
    def on_btn_new_group_clicked(self, button):
        dialog = NewGroupDialog()
        dialog.set_transient_for(parent=self)
        response = dialog.run()

        print(f'Resposta do diálogo = {response}.')

        # Verificando qual botão foi pressionado.
        if response == Gtk.ResponseType.YES:
            core = Core()
            core.description = dialog.newGroup()
            core.insertCore(core)

        elif response == Gtk.ResponseType.NO:
            print('Botão NÃO pressionado')

        elif response == Gtk.ResponseType.DELETE_EVENT:
            print('Botão de fechar a janela pressionado')

        dialog.destroy()

    @Gtk.Template.Callback()
    def on_btn_new_person_clicked(self, button):
        c = Character()
        c.name = "unnamed"
        c.insertCharacter(c)


    @Gtk.Template.Callback()
    def on_btn_group_category_clicked(self, widget):
        dialog = CapivaraSmartGroup()
        dialog.set_transient_for(parent=self)
        response = dialog.run()

        # Verificando qual botão foi pressionado.
        if response == Gtk.ResponseType.YES:
            print('Botão SIM pressionado')
            smartGroup = SmartGroup()
            smartGroup.description = dialog.newSmartGroup()
            smartGroup.insertSmartGroup(smartGroup)

        elif response == Gtk.ResponseType.NO:
            print('Botão NÃO pressionado')

        elif response == Gtk.ResponseType.DELETE_EVENT:
            print('Botão de fechar a janela pressionado')

        dialog.destroy()

    @Gtk.Template.Callback()
    def on_mnu_properties_project_clicked(self, widget):
        projectProperties = ProjectProperties()
        propriedades = projectProperties.get()
        dialog = ProjectPropertiesDialog(propriedades)
        dialog.set_transient_for(parent=self)
        response = dialog.run()

        # Verificando qual botão foi pressionado.
        if response == Gtk.ResponseType.YES:
            _projectProperties = dialog.properties()
            propriedades.title = _projectProperties['title']
            propriedades.authorsFullName = _projectProperties['authors full name']
            propriedades.surname = _projectProperties['surname']
            propriedades.forename = _projectProperties['forename']
            propriedades.pseudonym = _projectProperties['pseudonym']
            propriedades.update(propriedades)


            capivara = {'version model': '0.1.0', 'creator': 'Capivara 0.1.0', 'device': 'ELIZEU-PC',
                        'modified': '2021-08-19 14:08:59.496007',
                        'project properties': {'title': 'Deixa-me enterrar meu pai',
                                               'abbreviated title': 'Deixa-me enterrar meu pai',
                                               'authors full name': 'Elizeu Xavier', 'surname': 'Xavier',
                                               'forename': 'Elizeu', 'pseudonym': ''},
                        'character': [{"name": "unnamed"}], 'core': [], 'smart group': [], 'tag': []}


        elif response == Gtk.ResponseType.NO:
            pass

        dialog.destroy()

    @Gtk.Template.Callback()
    def menu_UpdadeVersion_clicked(self, widget):
        print("Menu update")
        # verificar se existe nova versãoo
        newVersion = True
        if newVersion:
            dialog = DialogUpdateAutomatically(self)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                print("The OK button was clicked")
            elif response == Gtk.ResponseType.CANCEL:
                print("The Cancel button was clicked")

            dialog.destroy()
        else:
            messagedialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO, \
                                              buttons=Gtk.ButtonsType.OK, text="Capivara is all up to date!")
            #     """ Assume you have it """
            scoreimg = Gtk.Image()
            scoreimg.set_from_file("assets/icons/information.png")  # or whatever its variant
            #     messagedialog.set_image(scoreimg)  # without the '', its a char
            messagedialog.set_title("Check for update")
            action_area = messagedialog.get_content_area()
            messagedialog.show_all()
            messagedialog.run()
            messagedialog.destroy()

    @Gtk.Template.Callback()
    def on_mnu_capivara_help_clicked(self, widget):
        webbrowser.open('file:/Program Files (x86)/MarinerSoftware/Persona/Help/Persona Help.html', new=2)

    @Gtk.Template.Callback()
    def on_mnu_PluginsManager_clicked(self, widget):
        dialog = PluginsManager()
        dialog.set_transient_for(parent=self)
        response = dialog.run()

        print(f'Resposta do diálogo = {response}.')

        # Verificando qual botão foi pressionado.
        if response == Gtk.ResponseType.YES:
            print('Botão SIM pressionado')
        elif response == Gtk.ResponseType.NO:
            print('Botão NÃO pressionado')

        elif response == Gtk.ResponseType.DELETE_EVENT:
            print('Botão de fechar a janela pressionado')

        dialog.destroy()

    @Gtk.Template.Callback()
    def about(self, widget):
        about = Gtk.AboutDialog.new()
        about.set_transient_for(parent=self)
        about.set_logo(logo=self.logo)
        about.set_program_name('Capivara')
        about.set_version('0.1.0')
        about.set_authors(authors=('Elizeu Ribeiro Sanches Xavier',))
        about.set_comments(
            comments='Criação do esboço de personagens de ficção'

        )
        about.set_website(website='https://github.com/ElizeuX/Capivara/wiki')
        about.run()
        about.destroy()

    # CALL BACK SEARCH
    def _show_hidden_search_bar(self):
        if self.search_bar.get_search_mode():
            self.search_bar.set_search_mode(search_mode=False)
        else:
            self.search_bar.set_search_mode(search_mode=True)

    def _change_button_state(self):
        if self._current_button_state:
            self.btn_search.set_state_flags(flags=Gtk.StateFlags.NORMAL, clear=True)
            self._current_button_state = False
        else:
            self.btn_search.set_state_flags(flags=Gtk.StateFlags.ACTIVE, clear=True)
            self._current_button_state = True

    @Gtk.Template.Callback()
    def on_btn_search_clicked(self, widget):
        self._current_button_state = widget.get_active()
        self._show_hidden_search_bar()

    @Gtk.Template.Callback()
    def key_press_event(self, widget, event):
        # shortcut = Gtk.accelerator_get_label(event.keyval, event.state)
        # if shortcut in ('Ctrl+F', 'Ctrl+Mod2+F'):
        #     self._show_hidden_search_bar()
        #     self._change_button_state()
        # if shortcut == 'Mod2+Esc' and self.search_bar.get_search_mode():
        #     self._show_hidden_search_bar()
        #     self._change_button_state()
        # return True
        pass

    # FIM CALL BACK SEARCH
    # status bar
    def statusbar_show_msg(self, msg):
        self.message_id = self.statusbar.push(
            context_id=self.context_id,
            text=msg,
        )

    def statusbar_remove_msg(self):
        # self.statusbar.remove(
        #     context_id=self.context_id,
        #     message_id=self.message_id,
        # )
        self.statusbar.remove_all(context_id=self.context_id)

    # status bar

    @Gtk.Template.Callback()
    def on_info_bar_button_clicked(self, widget, response):
        if response == Gtk.ResponseType.CLOSE:
            self.info_bar.set_revealed(revealed=False)

    def info_bar_timeout(self):
        self.info_bar.set_revealed(revealed=False)


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(application_id='br.elizeux.Capivara',
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                        **kwargs
                         )

        self.add_main_option(
            "test",
            ord("t"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Command line test",
            None,
        )

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):

        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)

        appConfig = AppConfig()

        win.set_title("Untitled")
        win.set_default_size(width=appConfig.getDefaultWidth(), height=appConfig.getDefaultHeight())
        win.set_position(position=Gtk.WindowPosition.CENTER)
        win.present()

        # Verifica se existe nova versão disponível
        if appConfig.getUpdateAutomatically() == "yes":
            # TODO: Criar função para verificar se existe nova versão disponível
            newVersion = True
            if newVersion:
                dialog = DialogUpdateAutomatically(win)
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    print("The OK button was clicked")
                elif response == Gtk.ResponseType.CANCEL:
                    print("The Cancel button was clicked")

                dialog.destroy()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        if "test" in options:
            # This is printed on the main instance
            print("Test argument recieved: %s" % options["test"])

        self.activate()
        return 0

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

# if __name__ == '__main__':
#     import sys
#
#     app = Application()
#     app.run(sys.argv)
