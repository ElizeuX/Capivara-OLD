# -*- coding: utf-8 -*-
"""Capivara"""

import gi

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gio, Gtk, GdkPixbuf, GLib

import Global
from Global import Global
from Utils import AppConfig, DialogUpdateAutomatically, DialogSelectFile, DialogSaveFile, DialogSelectImage, \
    DialogSaveRelationshipImage, Date
import PluginsManager
import webbrowser
from CapivaraSmartGroup import CapivaraSmartGroup
from DataAccess import DataUtils, ProjectProperties, Character, Core, SmartGroup, CharacterMap, Tag, TagCharacterLink
import Utils
from src.logger import Logs
from TreeviewCtrl import Treeview
from collections import namedtuple
import LoadCapivaraFile
import SaveCapivaraFile
from datetime import datetime
from Utils import JsonTools
import json
import os
from pathlib import Path
from Constants import Capivara

import LoadCharacterMap
import GraphTools

# importar Telas
from Preferences import Preferences
from ProjectPropertiesDialog import ProjectPropertiesDialog
from NewGroupDialog import NewGroupDialog
from PluginsManager import PluginsManager
from CapivaraPrint import PrintOperation

logs = Logs(filename="capivara.log")


@Gtk.Template(filename='MainWindow.ui')
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    settings = Gtk.Settings.get_default()
    flagDateEdit = False

    btn_search = Gtk.Template.Child(name='btn_search')
    search_bar = Gtk.Template.Child(name='search_bar')
    statusbar = Gtk.Template.Child(name='statusbar')
    header_bar = Gtk.Template.Child(name='header_bar')
    treeView = Gtk.Template.Child(name='treeview')
    scrollView = Gtk.Template.Child(name='scrollView')
    # spinner = Gtk.Template.Child(name='spinner')
    info_bar = Gtk.Template.Child(name='info_bar')
    list_store = Gtk.Template.Child(name='list_store')
    lstStoreMap = Gtk.Template.Child(name='lstStoreMap')
    imgCharacter = Gtk.Template.Child(name='imgCharacter')

    # campos da tela
    lblId = Gtk.Template.Child(name='lblId')
    txtName = Gtk.Template.Child(name='gtkEntryName')
    cboArchtype = Gtk.Template.Child(name='cboArchtype')
    txtDate = Gtk.Template.Child(name='gtkEntryDate')
    cboSex = Gtk.Template.Child(name='cboSex')
    txtHeigth = Gtk.Template.Child(name='gtkEntryHeigth')
    txtWeigth = Gtk.Template.Child(name='gtkEntryWeigth')
    txtBodyType = Gtk.Template.Child(name='gtkEntryBodyType')
    txtEyeColor = Gtk.Template.Child(name='gtkEntryEyeColor')
    txtHairColor = Gtk.Template.Child(name='gtkEntryHairColor')
    txtLocal = Gtk.Template.Child(name='gtkEntryLocal')
    txtEthinicity = Gtk.Template.Child(name='gtkEntryEthinicity')
    txtHealth = Gtk.Template.Child(name='gtkEntryHealth')
    txtTag = Gtk.Template.Child(name='gtkEntryTag')
    txtBackground = Gtk.Template.Child(name='txtBackground')
    imgCharacter = Gtk.Template.Child(name='imgCharacter')
    chkCharacter =Gtk.Template.Child(name='chkCharacter')
    chkCore = Gtk.Template.Child(name='chkCore')


    # Vo com os elementos da tela
    voCharacter = namedtuple('voCharacter',
                             ['id', 'name', 'archtype', 'date_of_birth', 'sex', 'height', 'weight', 'body_type',
                              'eye_color',
                              'hair_color', 'ethinicity', 'health', 'tag', 'local',
                              'background',
                              'picture', 'biography'])

    capivaraFile = ""

    # Obtendo as configurações
    appConfig = AppConfig()
    capivaraPathFile = appConfig.getCapivaraDirectory()
    version = appConfig.getCapivaraVersion()

    # Configurando globais
    Global.set("my_capivara", capivaraPathFile)
    Global.set("version", version)

    if appConfig.getDarkmode() == 'yes':
        settings.set_property('gtk-application-prefer-dark-theme', True)
    else:
        settings.set_property('gtk-application-prefer-dark-theme', False)

    logo = GdkPixbuf.Pixbuf.new_from_file(filename='assets/icons/icon.png')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.chkCharacter.set_active(True)
        self.chkCharacter.set_sensitive(False)
        self.chkCore.set_active(False)

        # IMAGEM INICIAL DO PERSONAGEM
        __NOIMAGE = '''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oooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAK2oX1vpmnXN/dyBLe2iaWRj2VRk/wAq+SPiV8SNQ8a6ttAe302E5t7Y+n95vViP0r1b9oLxcNP0S28N28uJ70iW4CnkRKflB+rDP/AfevmtmLMSepoATqaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDrfAnjnU/BetpeWLGRHwlxbM2EuE9D6MOzDkE9wSD9e+HdfsfE+g2usaezG3uV3BXGGQg4KsPUEEV8K17t+zx4uEOo3Xhe5k+W6BuLYH/noo+cD6qAf+AH1oA+iaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKrahfW+l6bdaheSeXbWsTzTPgnaigknA5PA7VZrzb4465/ZHw3urZH2zai62y4PO37zfouP8AgVAHzN4x8S3Hi7xVfazcZAnkPlIf+WcY4VfwGPxzWFRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABV/RNTudG1q01KzcJc20qyxsem4HIz6jjBHeqFFAH3Z4e1u28R+H7HWLQ/ubuISBc5KHoyn3BBB9xWnXjP7O+ufa/DGoaPI2Xs51mTJ/gkHIA9mUn/gVezUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAV82ftGa8bjxLp2ixP8lnAZJB/tydv++VB/wCBV9J18S+P9YfXfHWsXzMWV7pxGc5+QHao/wC+QKAOaooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA9N+BuvDSfiLZ2zuI4r6N7V8ngk/Mn47lUfjX1lXwZpWoS6VqltfwErNbyrLG3oysGB/MV912V3Ff2FveQHMVxEsqH1VgCP0NAFiiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAyfE2pDR/C+q6iW2m2tZJFP+0FOP1xXwxISZXJOSWO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zAa1fqdhB5gi5Bk+uRhffJ/hwfk+gAooooAKKKKACiiigAooooAKKKKACiiigArt/hFp51H4oaJGBlY5vPJ9NgL/APstcRXsf7O1ibnxpd3bZKWlo5X2Zyq/yDflQB9OUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB5l8eNKOpfDOeZRlrG4iuBgc4zsP4fPn8K+Ta+5/FeknXfCWraWqgvc2skcef7+07T/31ivhuUETOGBBDHIPWgBlFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH2h8LNMXSfhh4et1cv5lotySfWXMuPw34/Cul1LULfStMu9Ru3KW1rC88rAZIRQSeO/AqS0tYLGygs7aNY7eCNYokUYCqowAPoBXmfx+1l9L+Gz2kRAfUbmO3bDYIQZdiPX7gU+zUAfNXinxHe+LPEd5rN87GS4kJRC2REn8KDpwBx79epNY9FFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABX0r+znpgi8OarqmwL9onSAf8ATJP4mT9K+aq+yfhNpLaR8NdIjljKTTo1zJnqd7FlP8A3ztoA7aiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvj/4w+G/+Ed+IOoBI9lvdv9qgwMAq+S35MGH4V9gV5N8fPDEer+Cl1iNP9K0twcgdYnIVh+B2n2Ab1oA+WaKKKACiiigAooooAKKKKACiiigAooooAK2/BkEd1458P28q7o5dStkceoMqg1iVr+FL630vxjoeoXb+XbWuoQTzPtJ2osisxwOTwD0oA+6K+d/2l72F9R8O2KsPPhinmdfRXKBT+cbflXpH/C7fh5/0MP8A5JXH/wAbrwf41eKtG8XeM7W/0O7N1axWCQNIYmT5xJIxGGAPRh2oA84ooooAKKKKACiiigAooooAKKKKACiiigAooooA3/BXh+TxR4w03SIwcTzDzCP4UHLH8FBr7dijSGJIo1CRooVVA4AHQV4R+zp4WRLfUPE86ZlZvslvkfdAwXP45Ufga96oAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKxvFiW8ng7W0uhm3NjP5g/2dhzj3rZrlfiSzr8N/EBj6/Y3B+h6/pmgD4qooooAKKKKACiiigAooooAKKKKACiiigAorS0DQ77xLrtpo+mxh7u6fYgY4A4yWJ9AASfYV9c+B/hloHgiyi+z28d1qQX97fzIDIzd9vXYvsPxJPNAHxpRX3/VLVNI03W7NrTVLG3vLdusc8YcfUZ6H3FAHwbRXpvxc+F3/CC3seo6azSaHdybIw5y9vJgnyyf4gQCVPXAIPIy3mVABRRRQAUUUUAFFFFABRRRQAUUUUAFKpwwPoaSigD7G+D6W6/CzRGtgNrpIzH1bzG3fqP0rua80+BMkj/C+0DklVnlCZ7DOePxJr0ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArn/HUZl8AeIkAyf7NuCPwjY10FRXNvDd2sttcRrJDMhjkRujKRgg/hQB8C9Dg0+SJo8bu9e/XX7Okkmvu1tq0MelGTcrOC0yp/d24Ckjn5s+nFcJ8aPD1v4b8aQWVpHstzYQGP1IVfLyff5KAPOaKKKACiiigAooooAKKKKACiiigD2/8AZs0qOfxBreqsfntLaOBFI/56sST9f3WPxNfSFfOv7NN/BHqviHTmJ8+eCGdBjjbGzK36yrX0VQAUUUUAcn8TtNg1X4Z+IYJx8sdlJcKR1DRDzF/VRXxZX2x8RryCx+G3iSW4cIjadNECf7zoUUfizAfjXxPQAUUUUAFFFFABRRRQAUUUUAFFFFAD4VV540YsFZgCVGTjPYU0jBIPauu+FumrqvxL0K2aMSKLkSsrAEEIC5yD7LXqWofs6ynXN+n6tENNZw375T5sS55GAMMQOhyPpQB3/wAFofJ+Feknj940z4Hb96w/pXf1n6Jo9n4f0W10mwQpa2ybEBOSe5J9yST+NaFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAV86ftLWqJq/h+7AG+WCaMnvhWUj/0M19F18/ftMgbvC7dyLof+iaAPAaKKKACiiigAooooAKKKKACiiigDc8IeKLzwd4ntNbshveAkSRFiFlQjDKfqOnXBAPavsfwr4u0bxjpEeo6RdCRSB5kLYEkLf3XXsf0PYkV8OVZsdQvdMulutPvLi0uFGBLbytG4/EEGgD72prukUbSSMqIoLMzHAAHUk18Rf8J34w/6GvXP/BjN/wDFVU1DxPr+r2/2fUtc1O9gzny7m7kkXPrhiRQB6f8AGv4pW3iZl8OaFKZNMt5Q9xdKxC3Eg6Kvqg65PU4I4AJ8boooAKKKKACiiigAooooAKKKKACiiigD1T9n62Sf4lrK3WCzldfqcL/JjX1XXzJ+zjEreONQkIyV05wPb95HX03QAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABXz/+01/zK/8A29/+0a+gK8p/aA01rz4ex3KDDWl4js2OisGQ/hlloA+VqKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAPbf2blB8T6u+ORZ4z9XX/CvpKvBf2atOxZa9qbL96SKBG+gLN/Na96oAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArlfiTp39qfDjXrULuItGlCjuY8OP1WuqqK5gjuraW3lXdHKhRx6gjBoA+CJWLTOzHJLEk0yrWpWM2mapd2FwMT20zQyD0ZSQf1FVaACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKOpop0f+sX6igD61+Bunmy+GtvOVAa9uJZ+BjjOwf8AoFekVh+DdMOjeDNG09l2vBaRq4x/HtBb9Sa3KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAPmL4/+Ev7L8VRa9bRkW+ppmXHQTKAD9MrtPud1eO19p/EjwsPF/ge/01EDXSr59qe4lXoB9Rlf+BV8WsjIxV1KsOoIwaAEooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvQfg54U/4Sfx7ameLfZWP+lT7hkHaflX3y2PwzXn4G5gB34r60+CfhU+HvA0V5cR7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'''
        pixbuf = Utils.get_pixbuf_from_base64string(__NOIMAGE)
        pixbuf = pixbuf.scale_simple(170, 200, 2)
        self.imgCharacter.set_from_pixbuf(pixbuf)

        self.context_id = self.statusbar.get_context_id(
            context_description='exemplo',
        )

        self.statusbar_show_msg("Teste")

        # NOVA VERSÃO
        # TODO: Verificar se existe nova versão e apresentar no Info
        newVersion = False
        if not self.info_bar.get_revealed() and newVersion:
            self.info_bar.set_revealed(revealed=True)
            GLib.timeout_add_seconds(priority=0, interval=5, function=self.info_bar_timeout)

        # CONSTRUINDO O MENU POPOVER DINAMICAMENTE
        popover = Gtk.Template.Child(name='menu-popover')
        # menu_item = Gtk.MenuItem("Excluir Capivara")
        # popover.append(menu_item)
        # menu_item = Gtk.MenuItem("Imprimir Capivara")
        # popover.append(menu_item)

        # Carregar os comboboxies
        archetypes = [
            ("No archtype", "No archtype"),
            ("The Hero", "The Hero"),
            ("The Lover", "The Lover"),
            ("The Magician", "The Magician"),
            ("The Outlaw.", "The Outlaw"),
            ("The Explorer", "The Explorer"),
            ("The Sage", "The Sage"),
            ("The Innocent", "The Innocent"),
            ("The Creator", "The Creator"),
            ("The Ruler", "The Ruler"),
            ("The Caregiver", "The Caregiver"),
            ("The Everyman", "The Everyman"),
            ("The Jester", "The Jester"),
            ("Hero", "Hero"),
            ("Mentor", "Mentor"),
            ("Ally", "Ally"),
            ("Herald", "Herald"),
            ("Trickster", "Trickster"),
            ("Shapeshifter", "Shapeshifter"),
            ("Guardian", "Guardian"),
            ("Shadow", "Shadow"),
        ]
        self.cboArchtype.set_entry_text_column(0)
        self.cboArchtype.connect("changed", self.on_cboArchtype_changed)
        for archetype in archetypes:
            self.cboArchtype.append(archetype[0], archetype[1])

        sex = [("Male", "Male"),
               ("Female", "Female"),
               ]
        self.cboSex.set_entry_text_column(0)
        self.cboSex.connect("changed", self.on_cboSex_changed)
        for s in sex:
            self.cboSex.append(s[0], s[1])

        LoadCapivaraFile.loadCapivaraFile()
        self.putHeaderBar()

        # Passa os campos da tela para treeview
        vo = self.voCharacter(self.lblId, self.txtName, self.cboArchtype, self.txtDate, self.cboSex, self.txtHeigth,
                              self.txtWeigth, self.txtBodyType, self.txtEyeColor, self.txtHairColor, self.txtEthinicity,
                              self.txtHealth, self.txtTag, self.txtLocal, self.txtBackground, self.imgCharacter,
                              self.list_store)

        Treeview(self.treeView, self, vo)

    @Gtk.Template.Callback()
    def on_btnEditPhoto_clicked(self, widget):
        dialog = DialogSelectImage(select_multiple=1)
        dialog.set_transient_for(parent=self)

        # Executando a janela de dialogo e aguardando uma resposta.
        response = dialog.run()

        # Verificando a resposta recebida.
        if response == Gtk.ResponseType.OK:
            logs.record("Abrindo arquivo de imagem : " + dialog.show_file_info(), type="info", colorize=True)
            fileOpen = dialog.show_file_info()
            stringBase64 = Utils.imageToBase64(self, fileOpen)
            pixbuf = Utils.get_pixbuf_from_base64string(stringBase64)
            pixbuf = pixbuf.scale_simple(170, 200, 2)
            self.imgCharacter.set_from_pixbuf(pixbuf)
            c = Character()
            intId = int(self.lblId.get_text().replace('#', '0'))
            c.set_image(intId, stringBase64)

        elif response == Gtk.ResponseType.NO:
            pass

        # Destruindo a janela de dialogo.
        dialog.destroy()

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
            logs.record("Abrindo arquivo : " + dialog.show_file_info(), type="info", colorize=True)

            # Carregar Capivara salva
            capivaraFile = dialog.show_file_info()

            try:
                dialog.destroy()

                # TODO: Colocar um spinner indicando  que o arquivo está sendo carregado

                LoadCapivaraFile.loadCapivaraFile(capivaraFile)
                #self.capivaraPathFile = os.path.dirname(os.path.realpath(capivaraFile))

                self.LoadRelationships()
                Global.set("capivara_file_open", capivaraFile)

                # Passa os campos da tela para treeview
                vo = self.voCharacter(self.lblId, self.txtName, self.cboArchtype, self.txtDate, self.cboSex,
                                      self.txtHeigth,
                                      self.txtWeigth, self.txtBodyType,
                                      self.txtEyeColor, self.txtHairColor, self.txtEthinicity, self.txtHealth,
                                      self.txtTag, self.txtLocal, self.txtBackground, self.imgCharacter,
                                      self.list_store)

                Treeview(self.treeView, self, vo)

                # Coloca nome do projeto e autor na header bar
                # projectProperties = ProjectProperties.get()
                # self.header_bar.set_title(projectProperties.title)
                # self.header_bar.set_subtitle(projectProperties.surname + ', ' + projectProperties.forename)
                # Global.set("title", projectProperties.title)
                self.putHeaderBar()

            except:
                logs.record("Não foi possível abrir o arquivo %s" % capivaraFile)
                dialog.destroy()
                self.messagebox("error", "Erro",
                                "Não foi possível carregar o arquivo %s" % os.path.basename(capivaraFile))

            finally:
                pass

        else:
            logs.record("Não foi aberto um novo arquivo.", type="info", colorize=True)
            dialog.destroy()

    @Gtk.Template.Callback()
    def on_btnViewGraph_clicked(self, widget):
        GraphTools.GraphMake(self.chkCharacter.get_active(), self.chkCore.get_active())

    @Gtk.Template.Callback()
    def on_btnSaveGraph_clicked(self, widget):
        dialog = DialogSaveRelationshipImage()
        dialog.set_transient_for(parent=self)

        # Executando a janela de dialogo e aguardando uma resposta.
        response = dialog.run()

        # Verificando a resposta recebida.
        if response == Gtk.ResponseType.OK:
            logs.record("Salvando o gráfico de relacionamento entre personagens: " + dialog.save_file(), type="info",
                        colorize=True)

            __fileOpen__ = dialog.save_file()

            dialog.destroy()

            try:
                GraphTools.GraphMake(self.chkCharacter.get_active(), self.chkCore.get_active(), __fileOpen__)

            except:
                pass

            finally:
                pass
        else:
            logs.record("Operação de salvar gráfico cancelada.", type="info", colorize=True)
            dialog.destroy()

    @Gtk.Template.Callback()
    def on_cellrender_relationship_edited(self, widget, row, value):
        self.lstStoreMap[row][2] = value
        c = CharacterMap()
        c.set_relationship(self.lstStoreMap[row][0], value)

    # ATUALIZAÇÃO DOS CAMPOS DA TELA
    @Gtk.Template.Callback()
    def on_gtkEntryName_focus_out_event(self, widget, event):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        c.set_name(intId, self.txtName.get_text())
        self.LoadRelationships()

        tree_selection = self.treeView.get_selection()
        (model, pathlist) = tree_selection.get_selected_rows()
        value = ""
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 2)
        if value:
            c = Character()
            c = c.get(value)
            model.set_value(tree_iter, 0, c.name)

    @Gtk.Template.Callback()
    def on_cboArchtype_changed(self, combo):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        text = combo.get_active_text()
        if text is not None:
            c.set_archtype(intId, text)

    @Gtk.Template.Callback()
    def on_cboSex_changed(self, combo):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        text = combo.get_active_text()
        if text is not None:
            c.set_sex(intId, text)


    @Gtk.Template.Callback()
    def on_gtkEntryDate_focus_out_event(self, widget, event):
        date = self.txtDate.get_text()
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        if date:
            date = Date.stringToDate(date)
            if Date.isValidDate(date):
                self.txtDate.set_text(date)
                c.set_dateOfBirth(intId, datetime.strptime(date, "%d/%m/%Y"))
            else:
                c = c.get(intId)
                date = c.date_of_birth
                self.txtDate.set_text(date.strftime('%m/%d/%Y'))
                self.messagebox("error", "ERRO", "Data inválida!")

    @Gtk.Template.Callback()
    def on_gtkEntryDate_focus_in_event(self, widget, event):
        date = self.txtDate.get_text()
        if date:
            strDate = Date.dateToString(date)
            self.txtDate.set_text(strDate)

    @Gtk.Template.Callback()
    def on_gtkEntryHeigth_focus_out_event(self, widget, event):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        c.set_height(intId, self.txtHeigth.get_text())

    @Gtk.Template.Callback()
    def on_gtkEntryWeigth_focus_out_event(self, widget, event):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        c.set_weight(intId, self.txtWeigth.get_text())

    @Gtk.Template.Callback()
    def on_gtkEntryBodyType_focus_out_event(self, widget, event):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        c.set_bodyType(intId, self.txtBodyType.get_text())

    @Gtk.Template.Callback()
    def on_gtkEntryEyeColor_focus_out_event(self, widget, event):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        c.set_eyeColor(intId, self.txtEyeColor.get_text())

    @Gtk.Template.Callback()
    def on_gtkEntryHairColor_focus_out_event(self, widget, event):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        c.set_hairColor(intId, self.txtHairColor.get_text())

    @Gtk.Template.Callback()
    def on_gtkEntryEthinicity_focus_out_event(self, widget, event):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        c.set_ethinicity(intId, self.txtEthinicity.get_text())

    @Gtk.Template.Callback()
    def on_gtkEntryHealth_focus_out_event(self, widget, event):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        c.set_health(intId, self.txtHealth.get_text())

    @Gtk.Template.Callback()
    def on_txtBackground_focus_out_event(self, widget, event):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        textbuffer = self.txtBackground.get_buffer()
        first_iter = textbuffer.get_start_iter()
        end_iter = textbuffer.get_end_iter()
        c.set_background(intId, textbuffer.get_text(first_iter, end_iter, False))

    @Gtk.Template.Callback()
    def on_gtkEntryTag_focus_out_event(self, widget, event):
        print(self.txtTag.get_text())
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        c = c.get(intId)

        tags = self.txtTag.get_text()
        lstTags = tags.split()
        for tag in lstTags:
            t = Tag()
            d = TagCharacterLink()
            if not t.hasTag(tag):
                t.description = tag
                t.insertTag(t)
                d.character_id = intId
                d.tag_id = t.getTag(tag).id
                d.insertTagCharacterLink(d)
            elif not c.hasTag(intId, tag):
                d = TagCharacterLink()
                d.character_id = intId
                d.tag_id = t.getTag(tag).id
                d.insertTagCharacterLink(d)












    @Gtk.Template.Callback()
    def on_gtkEntryLocal_focus_out_event(self, widget, event):
        c = Character()
        intId = int(self.lblId.get_text().replace('#', '0'))
        c.set_local(intId, self.txtLocal.get_text())

    @Gtk.Template.Callback()
    def on_btn_new_project_clicked(self, widget):

        projectProperties = ProjectProperties()
        projectProperties.title = ""
        projectProperties.authorsFullName = ""
        projectProperties.surname = ""
        projectProperties.forename = ""
        projectProperties.pseudonym = ""


        LoadCapivaraFile.loadCapivaraFile()

        self.putHeaderBar()

        # Passa os campos da tela para treeview
        vo = self.voCharacter(self.lblId, self.txtName, self.cboArchtype, self.txtDate, self.cboSex, self.txtHeigth,
                              self.txtWeigth, self.txtBodyType, self.txtEyeColor, self.txtHairColor,
                              self.txtEthinicity,
                              self.txtHealth, self.txtTag, self.txtLocal, self.txtBackground, self.imgCharacter,
                              self.list_store)
        Treeview(self.treeView, self, vo)

        # projectProperties = ProjectProperties()
        # projectProperties.title = ""
        # projectProperties.authorsFullName = ""
        # projectProperties.surname = ""
        # projectProperties.forename = ""
        # projectProperties.pseudonym = ""
        #
        # dialog = ProjectPropertiesDialog(projectProperties)
        # dialog.set_transient_for(parent=self)
        # response = dialog.run()
        #
        # # Verificando qual botão foi pressionado.
        # if response == Gtk.ResponseType.YES:
        #     # projectProject = dialog.properties()
        #     # dataUtils = DataUtils()
        #     # dataUtils.LoadCapivaraFileEmpty(projectProject)
        #     # capivara = {'version model': '0.1.0', 'creator': 'Capivara 0.1.0', 'device': 'ELIZEU-PC',
        #     #             'modified': '2021-08-19 14:08:59.496007',
        #     #             'project properties': {'title': 'Deixa-me enterrar meu pai',
        #     #                                    'abbreviated title': 'Deixa-me enterrar meu pai',
        #     #                                    'authors full name': 'Elizeu Xavier', 'surname': 'Xavier',
        #     #                                    'forename': 'Elizeu', 'pseudonym': ''},
        #     #             'character': [{"name": "unnamed"}], 'core': [], 'smart group': [], 'tag': []}
        #     # Treeview(self.treeView, capivara)
        #
        #
        #
        # elif response == Gtk.ResponseType.NO:
        #     pass
        #
        # dialog.destroy()

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

        try:
            # Pegar o nome do projeto
            c = ProjectProperties()
            c = c.get()
            if c.title:
                SaveCapivaraFile.saveCapivaraFile(self.capivaraPathFile + '/' + c.title + '.capivara')
            else:
                dialog = DialogSaveFile()
                dialog.set_transient_for(parent=self)
                response = dialog.run()

                # Verificando a resposta recebida.
                if response == Gtk.ResponseType.OK:
                    capivaraFile = dialog.save_file()
                    dialog.destroy()
                    try:
                        c = ProjectProperties()
                        c = c.get()
                        c.title = Path(capivaraFile).stem
                        c.update(c)
                        SaveCapivaraFile.saveCapivaraFile(capivaraFile)

                        logs.record("Arquivo salvo com sucesso!", type="info")
                        self.messagebox(Gtk.MessageType.INFO, "INFORMATION",
                                        "O arquivo %s foi salvo com sucesso." % os.path.basename(capivaraFile))

                        LoadCapivaraFile.loadCapivaraFile(capivaraFile)
                        Global.set("capivara_file_open", capivaraFile)

                        self.LoadRelationships()

                        # # Coloca nome do projeto e autor na header bar
                        self.putHeaderBar()
                        # projectProperties = ProjectProperties.get()
                        # self.header_bar.set_title(projectProperties.title)
                        # self.header_bar.set_subtitle(projectProperties.surname + ', ' + projectProperties.forename)


                    except:
                        logs.record("Não foi possível salvar o arquivo %s" % capivaraFile)
                        self.messagebox("error", "ERRO",
                                        "Não foi possível salvar o arquivo %s" % os.path.basename(self.capivaraFile))

                else:
                    dialog.destroy()
                    logs.record("Salvar como cancelado.", type="info", colorize=True)


        except:
            logs.record("Não foi possível salvar o arquivo")
            self.messagebox("error", "ERRO",
                            "Não foi possível salvar o arquivo %s" % os.path.basename(self.capivaraFile))

    # SALVAR COMO
    @Gtk.Template.Callback()
    def on_btn_save_as_clicked(self, widget):

        dialog = DialogSaveFile()
        dialog.set_transient_for(parent=self)
        response = dialog.run()

        # Verificando a resposta recebida.
        if response == Gtk.ResponseType.OK:

            capivaraFile = dialog.save_file()

            dialog.destroy()

            try:
                c = ProjectProperties()
                c = c.get()
                c.title = Path(capivaraFile).stem
                c.update(c)

                SaveCapivaraFile.saveCapivaraFile(capivaraFile)

                logs.record("Arquivo salvo com sucesso!", type="info")
                self.messagebox(Gtk.MessageType.INFO, "INFORMATION",
                                "O arquivo %s foi salvo com sucesso." % os.path.basename(capivaraFile))

                LoadCapivaraFile.loadCapivaraFile(capivaraFile)
                Global.set("capivara_file_open", capivaraFile)

                self.LoadRelationships()

                # # Coloca nome do projeto e autor na header bar
                self.putHeaderBar()
                # projectProperties = ProjectProperties.get()
                # self.header_bar.set_title(projectProperties.title)
                # self.header_bar.set_subtitle(projectProperties.surname + ', ' + projectProperties.forename)


            except:
                logs.record("Não foi possível salvar o arquivo %s" % capivaraFile)
                self.messagebox("error", "ERRO",
                                "Não foi possível salvar o arquivo %s" % os.path.basename(self.capivaraFile))

        else:
            dialog.destroy()
            logs.record("Salvar como cancelado.", type="info", colorize=True)

    @Gtk.Template.Callback()
    def menu_item_clicked(self, widget):
        print(widget.props)

    @Gtk.Template.Callback()
    def on_mnuCapivaraPrint_clicked(self, button):
        self.builder = Gtk.Builder.new_from_file('CapivaraPrint.ui')
        self.builder.connect_signals(self)
        window = self.builder.get_object('CapivaraPrint')
        # window = Gtk.Window.new(type=Gtk.WindowType.TOPLEVEL)
        window.set_transient_for(parent=self)
        window.set_modal(modal=True)
        window.set_title(title='Gtk.Window')
        window.set_default_size(width=800, height=600)
        # window.set_default_icon_from_file(filename='../../../assets/icons/person.png')
        window.show_all()
        self.text_buffer_print = Gtk.Template.Child(name='text_buffer_print')
        self.text_view_print = Gtk.Template.Child(name='text_view_print')

        textbuffer = self.text_view_print
        textbuffer.set_text("This is some text ")

        # start_iter = self.text_buffer_print.get_start_iter()
        #
        # self.text_buffer_print.insert(start_iter, "This is some text ")
        # self.text_buffer_print.insert_markup(self.text_buffer_print.get_end_iter(), "<b>and some bold text</b>", -1)

        text = """<span size="xx-large">Lorem</span>
        Lorem <b>ipsum</b> <span foreground="red">dolor</span> <big>sit</big> amet,
        <i>consectetur</i> adipiscing <s>elit</s>, sed <sub>do</sub> 
        <span background="green">eiusmod</span> <sup>tempor</sup> incididunt 
        <small>ut</small> <tt>labore</tt> et <u>dolore</u> magna aliqua.
        <span size="xx-large">Lorem</span>
        Lorem <b>ipsum</b> <span foreground="red">dolor</span> <big>sit</big> amet,
        <i>consectetur</i> adipiscing <s>elit</s>, sed <sub>do</sub> 
        <span background="green">eiusmod</span> <sup>tempor</sup> incididunt 
        <small>ut</small> <tt>labore</tt> et <u>dolore</u> magna aliqua.\n
        """
        # self.text_buffer_print.insert_markup(self.textbuffer.get_end_iter(), text, -1)
        # # Adicionando texto renderizado ao Gtk.TextView.
        # text_buffer_iter = self.text_buffer_print.get_end_iter()
        # self.text_buffer_print.insert_markup(
        #     iter=text_buffer_iter,
        #     markup=text,
        #     len=-1,
        # )

    # @Gtk.Template.Callback()
    # def open_print_dialog(self, widget):
    #     """Dialogo de impressão do sistema."""
    #
    #     # Variável auxilizar com as configurações do papel.
    #     page_setup = PrintOperation.page_setup(self)
    #
    #     print_operation = PrintOperation(text_buffer=self.text_buffer_print)
    #     print_operation.set_default_page_setup(default_page_setup=page_setup)
    #
    #     # Resposta da operação de impressão.
    #     response = print_operation.run(action=Gtk.PrintOperationAction.PRINT_DIALOG, parent=self)
    #     if response == Gtk.PrintOperationResult.ERROR:
    #         print('ERROR')
    #     elif response == Gtk.PrintOperationResult.APPLY:
    #         print('APPLY')
    #     elif response == Gtk.PrintOperationResult.CANCEL:
    #         print('CANCEL')
    #     elif response == Gtk.PrintOperationResult.IN_PROGRESS:
    #         print('IN_PROGRESS')

    # @Gtk.Template.Callback()
    # def open_preview(self, widget):
    #
    #     """Pré visualizador do sistema."""
    #     print_operation = PrintOperation(text_buffer=self.text_buffer_print)
    #     response = print_operation.run(action=Gtk.PrintOperationAction.PREVIEW, parent=self)
    #
    # @Gtk.Template.Callback()
    # def open_page_setup_dialog(self, widget):
    #     """Diálogo para configuração da página."""
    #
    #     # Verificando o tamanho da página ANTES do diálogo.
    #     print(self.page_setup.get_page_width(unit=Gtk.Unit.MM))
    #     self.page_setup = Gtk.print_run_page_setup_dialog(
    #         parent=self,
    #         page_setup=self.page_setup,
    #         settings=self.print_settings,
    #     )
    #     # Verificando o tamanho da página DEPOIS do diálogo.
    #     print(self.page_setup.get_page_width(unit=Gtk.Unit.MM))
    #
    # @Gtk.Template.Callback()
    # def export_to_pdf(self, widget):
    #     """Exportando para arquivo."""
    #     print_operation = PrintOperation(text_buffer=self.text_buffer)
    #     print_operation.set_export_filename('nome-do-arquivo.pdf')
    #     response = print_operation.run(action=Gtk.PrintOperationAction.EXPORT, parent=self)
    #     if response == Gtk.PrintOperationResult.APPLY:
    #         print('Arquivo exportado com sucesso')

    @Gtk.Template.Callback()
    def on_btn_new_group_clicked(self, button):
        dialog = NewGroupDialog()
        dialog.set_transient_for(parent=self)
        response = dialog.run()

        # Verificando qual botão foi pressionado.
        if response == Gtk.ResponseType.YES:
            core = Core()
            core.description = dialog.newGroup()
            core.insertCore(core)
            Treeview(self.treeView, self)

        dialog.destroy()

    @Gtk.Template.Callback()
    def on_btn_new_person_clicked(self, button):
        c = Character()
        c.name = "unnamed"
        c.archtype = ""
        c.sex = ""
        c.local = ""
        c.occupation = ""
        c.position_social = ""
        c.height = 0.00
        c.weight = 0.00
        c.body_type = ""
        c.appearance = ""
        c.eye_color = ""
        c.hair_color = ""
        c.ethnicity = ""
        c.health = ""
        c.standing_features = ""
        c.background = ""
        c.hobbies = ""
        c.picture = '''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oooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAK2oX1vpmnXN/dyBLe2iaWRj2VRk/wAq+SPiV8SNQ8a6ttAe302E5t7Y+n95vViP0r1b9oLxcNP0S28N28uJ70iW4CnkRKflB+rDP/AfevmtmLMSepoATqaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDrfAnjnU/BetpeWLGRHwlxbM2EuE9D6MOzDkE9wSD9e+HdfsfE+g2usaezG3uV3BXGGQg4KsPUEEV8K17t+zx4uEOo3Xhe5k+W6BuLYH/noo+cD6qAf+AH1oA+iaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKrahfW+l6bdaheSeXbWsTzTPgnaigknA5PA7VZrzb4465/ZHw3urZH2zai62y4PO37zfouP8AgVAHzN4x8S3Hi7xVfazcZAnkPlIf+WcY4VfwGPxzWFRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABV/RNTudG1q01KzcJc20qyxsem4HIz6jjBHeqFFAH3Z4e1u28R+H7HWLQ/ubuISBc5KHoyn3BBB9xWnXjP7O+ufa/DGoaPI2Xs51mTJ/gkHIA9mUn/gVezUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAV82ftGa8bjxLp2ixP8lnAZJB/tydv++VB/wCBV9J18S+P9YfXfHWsXzMWV7pxGc5+QHao/wC+QKAOaooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA9N+BuvDSfiLZ2zuI4r6N7V8ngk/Mn47lUfjX1lXwZpWoS6VqltfwErNbyrLG3oysGB/MV912V3Ff2FveQHMVxEsqH1VgCP0NAFiiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAyfE2pDR/C+q6iW2m2tZJFP+0FOP1xXwxISZXJOSWO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zAa1fqdhB5gi5Bk+uRhffJ/hwfk+gAooooAKKKKACiiigAooooAKKKKACiiigArt/hFp51H4oaJGBlY5vPJ9NgL/APstcRXsf7O1ibnxpd3bZKWlo5X2Zyq/yDflQB9OUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB5l8eNKOpfDOeZRlrG4iuBgc4zsP4fPn8K+Ta+5/FeknXfCWraWqgvc2skcef7+07T/31ivhuUETOGBBDHIPWgBlFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH2h8LNMXSfhh4et1cv5lotySfWXMuPw34/Cul1LULfStMu9Ru3KW1rC88rAZIRQSeO/AqS0tYLGygs7aNY7eCNYokUYCqowAPoBXmfx+1l9L+Gz2kRAfUbmO3bDYIQZdiPX7gU+zUAfNXinxHe+LPEd5rN87GS4kJRC2REn8KDpwBx79epNY9FFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABX0r+znpgi8OarqmwL9onSAf8ATJP4mT9K+aq+yfhNpLaR8NdIjljKTTo1zJnqd7FlP8A3ztoA7aiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvj/4w+G/+Ed+IOoBI9lvdv9qgwMAq+S35MGH4V9gV5N8fPDEer+Cl1iNP9K0twcgdYnIVh+B2n2Ab1oA+WaKKKACiiigAooooAKKKKACiiigAooooAK2/BkEd1458P28q7o5dStkceoMqg1iVr+FL630vxjoeoXb+XbWuoQTzPtJ2osisxwOTwD0oA+6K+d/2l72F9R8O2KsPPhinmdfRXKBT+cbflXpH/C7fh5/0MP8A5JXH/wAbrwf41eKtG8XeM7W/0O7N1axWCQNIYmT5xJIxGGAPRh2oA84ooooAKKKKACiiigAooooAKKKKACiiigAooooA3/BXh+TxR4w03SIwcTzDzCP4UHLH8FBr7dijSGJIo1CRooVVA4AHQV4R+zp4WRLfUPE86ZlZvslvkfdAwXP45Ufga96oAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKxvFiW8ng7W0uhm3NjP5g/2dhzj3rZrlfiSzr8N/EBj6/Y3B+h6/pmgD4qooooAKKKKACiiigAooooAKKKKACiiigAorS0DQ77xLrtpo+mxh7u6fYgY4A4yWJ9AASfYV9c+B/hloHgiyi+z28d1qQX97fzIDIzd9vXYvsPxJPNAHxpRX3/VLVNI03W7NrTVLG3vLdusc8YcfUZ6H3FAHwbRXpvxc+F3/CC3seo6azSaHdybIw5y9vJgnyyf4gQCVPXAIPIy3mVABRRRQAUUUUAFFFFABRRRQAUUUUAFKpwwPoaSigD7G+D6W6/CzRGtgNrpIzH1bzG3fqP0rua80+BMkj/C+0DklVnlCZ7DOePxJr0ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArn/HUZl8AeIkAyf7NuCPwjY10FRXNvDd2sttcRrJDMhjkRujKRgg/hQB8C9Dg0+SJo8bu9e/XX7Okkmvu1tq0MelGTcrOC0yp/d24Ckjn5s+nFcJ8aPD1v4b8aQWVpHstzYQGP1IVfLyff5KAPOaKKKACiiigAooooAKKKKACiiigD2/8AZs0qOfxBreqsfntLaOBFI/56sST9f3WPxNfSFfOv7NN/BHqviHTmJ8+eCGdBjjbGzK36yrX0VQAUUUUAcn8TtNg1X4Z+IYJx8sdlJcKR1DRDzF/VRXxZX2x8RryCx+G3iSW4cIjadNECf7zoUUfizAfjXxPQAUUUUAFFFFABRRRQAUUUUAFFFFAD4VV540YsFZgCVGTjPYU0jBIPauu+FumrqvxL0K2aMSKLkSsrAEEIC5yD7LXqWofs6ynXN+n6tENNZw375T5sS55GAMMQOhyPpQB3/wAFofJ+Feknj940z4Hb96w/pXf1n6Jo9n4f0W10mwQpa2ybEBOSe5J9yST+NaFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAV86ftLWqJq/h+7AG+WCaMnvhWUj/0M19F18/ftMgbvC7dyLof+iaAPAaKKKACiiigAooooAKKKKACiiigDc8IeKLzwd4ntNbshveAkSRFiFlQjDKfqOnXBAPavsfwr4u0bxjpEeo6RdCRSB5kLYEkLf3XXsf0PYkV8OVZsdQvdMulutPvLi0uFGBLbytG4/EEGgD72prukUbSSMqIoLMzHAAHUk18Rf8J34w/6GvXP/BjN/wDFVU1DxPr+r2/2fUtc1O9gzny7m7kkXPrhiRQB6f8AGv4pW3iZl8OaFKZNMt5Q9xdKxC3Eg6Kvqg65PU4I4AJ8boooAKKKKACiiigAooooAKKKKACiiigD1T9n62Sf4lrK3WCzldfqcL/JjX1XXzJ+zjEreONQkIyV05wPb95HX03QAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABXz/+01/zK/8A29/+0a+gK8p/aA01rz4ex3KDDWl4js2OisGQ/hlloA+VqKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAPbf2blB8T6u+ORZ4z9XX/CvpKvBf2atOxZa9qbL96SKBG+gLN/Na96oAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArlfiTp39qfDjXrULuItGlCjuY8OP1WuqqK5gjuraW3lXdHKhRx6gjBoA+CJWLTOzHJLEk0yrWpWM2mapd2FwMT20zQyD0ZSQf1FVaACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKOpop0f+sX6igD61+Bunmy+GtvOVAa9uJZ+BjjOwf8AoFekVh+DdMOjeDNG09l2vBaRq4x/HtBb9Sa3KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAPmL4/+Ev7L8VRa9bRkW+ppmXHQTKAD9MrtPud1eO19p/EjwsPF/ge/01EDXSr59qe4lXoB9Rlf+BV8WsjIxV1KsOoIwaAEooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvQfg54U/4Sfx7ameLfZWP+lT7hkHaflX3y2PwzXn4G5gB34r60+CfhU+HvA0V5cR7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'''
        c.notes = ""
        c.insertCharacter(c)

        characterOne = c.id
        characterTwos = c.list()
        for characterTwo in characterTwos:
            if characterOne != characterTwo.id:
                cm = CharacterMap()
                cm.character_one = characterOne
                cm.character_relationship = ""
                cm.character_two = characterTwo.id
                cm.insertCharacterMap(cm)
                cm = CharacterMap()
                cm.character_one = characterTwo.id
                cm.character_relationship = ""
                cm.character_two = characterOne
                cm.insertCharacterMap(cm)

        self.LoadRelationships()
        Treeview(self.treeView, self)

    def LoadRelationships(self):
        self.lstStoreMap.clear()
        cmaps = CharacterMap()
        cmaps = cmaps.list()
        c = Character()
        lstCharacterMap = []
        for cm in cmaps:
            characterOneId = cm.character_one
            characterTwoId = cm.character_two
            tplCharacterMap = (cm.id, c.get(characterOneId).name, cm.character_relationship, c.get(characterTwoId).name)
            lstCharacterMap.append(tplCharacterMap)

        for relationship in lstCharacterMap:
            self.lstStoreMap.append(row=relationship)

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
            smartGroup.rule = "a = a"
            smartGroup.insertSmartGroup(smartGroup)

            Treeview(self.treeView, self)

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

            # Atualiza a barra de título
            self.header_bar.set_title(propriedades.title)
            self.header_bar.set_subtitle(propriedades.surname + ', ' + propriedades.forename)

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

    def messagebox(self, parMessage_type=None, msg1="Info", msg2=""):
        messageType = Gtk.MessageType.INFO
        buttonsType = Gtk.ButtonsType.OK
        if parMessage_type == "info":
            pass
        elif parMessage_type == "error":
            messageType = Gtk.MessageType.ERROR
            buttonsType = Gtk.ButtonsType.CANCEL
        elif parMessage_type == "warn":
            messageType = Gtk.MessageType.WARNING
            buttonsType = Gtk.ButtonsType.OK_CANCEL

        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=messageType,
            buttons=buttonsType,
            text=msg1,
        )
        dialog.format_secondary_text(msg2)
        dialog.run()
        dialog.destroy()
        return 0

    def putHeaderBar(self):
        # Coloca nome do projeto e autor na header bar
        projectProperties = ProjectProperties.get()
        if not projectProperties.title:
            self.header_bar.set_title("Capivara")
            self.header_bar.set_subtitle("version %s" % Global.config("version"))
            Global.set("title", projectProperties.title)
        else:
            self.header_bar.set_title(projectProperties.title)
            self.header_bar.set_subtitle(projectProperties.surname + ', ' + projectProperties.forename)
            Global.set("title", projectProperties.title)

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
        appConfig = AppConfig()
        cfgWidth = appConfig.getDefaultWidth()
        cfgHeight = appConfig.getDefaultHeight()

        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)

        win.set_title("Capivara")
        win.set_default_size(cfgWidth, cfgHeight)
        win.set_position(Gtk.WindowPosition.CENTER)
        win.present()

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

