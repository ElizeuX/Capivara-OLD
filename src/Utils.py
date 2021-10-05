# -*- coding: utf-8 -*-
import base64


import gi

from logger import Logs

gi.require_version(namespace='Gtk', version='3.0')
from gi.repository import Gtk, GdkPixbuf

import configparser
from pathlib import Path
import importlib
import os
import json
import datetime
import secrets
import uuid
from Global import Global
from CapivaraError import CapivaraDoesNotExistError, CapivaraDecodeFailError

PluginFolder = "../plugins/"
MainModule = "__init__"



class DialogSelectAeon(Gtk.FileChooserDialog):
    # Definindo o diretório padrão.
    home = Path.home()


    def __init__(self):
        super().__init__()
        self.select_multiple = False

        self.set_title(title='Abrir Projeto AeonTimeLine')
        self.set_modal(modal=True)

        #
        # Tipo de ação que o dialogo irá executar.
        self.set_action(action=Gtk.FileChooserAction.OPEN)

        # Defininido se a seleção será multipla ou não
        self.set_select_multiple(select_multiple=self.select_multiple)
        # Pasta onde o diálogo será aberto.
        self.set_current_folder(filename=str(self.home))

        # Botões que serão exibidos.
        self.add_buttons(
            '_Cancelar', Gtk.ResponseType.CANCEL,
            '_OK', Gtk.ResponseType.OK
        )

        # Adicionando class action nos botões.
        # btn_cancel = self.get_widget_for_response(
        #     response_id=Gtk.ResponseType.CANCEL,
        # )
        # btn_cancel.get_style_context().add_class(class_name='destructive-action')
        #
        # btn_save = self.get_widget_for_response(
        #     response_id=Gtk.ResponseType.OK,
        # )
        # btn_save.get_style_context().add_class(class_name='suggested-action')

        # Criando e adicionando filtros.
        aeon_filter = Gtk.FileFilter()
        aeon_filter.set_name("Aeon Timeline 2 (*.aeonzip)")
        aeon_filter.add_pattern("*.aeonzip")
        self.add_filter(filter=aeon_filter)

        # É obrigatório utilizar ``show_all()``.
        self.show_all()

    def show_file_info(self):
        return self.get_filename()

class DialogSelectScrivener(Gtk.FileChooserDialog):
    # Definindo o diretório padrão.
    home = Path.home()

    def __init__(self):
        super().__init__()
        self.select_multiple = False

        self.set_title(title='Abrir Projeto Scrivener')
        self.set_modal(modal=True)

        #
        # Tipo de ação que o dialogo irá executar.
        self.set_action(action=Gtk.FileChooserAction.OPEN)

        # Defininido se a seleção será multipla ou não
        self.set_select_multiple(select_multiple=self.select_multiple)
        # Pasta onde o diálogo será aberto.
        self.set_current_folder(filename=str(self.home))

        # Botões que serão exibidos.
        self.add_buttons(
            '_Cancelar', Gtk.ResponseType.CANCEL,
            '_OK', Gtk.ResponseType.OK
        )

        # Adicionando class action nos botões.
        # btn_cancel = self.get_widget_for_response(
        #     response_id=Gtk.ResponseType.CANCEL,
        # )
        # btn_cancel.get_style_context().add_class(class_name='destructive-action')
        #
        # btn_save = self.get_widget_for_response(
        #     response_id=Gtk.ResponseType.OK,
        # )
        # btn_save.get_style_context().add_class(class_name='suggested-action')

        # Criando e adicionando filtros.
        scrivx_filter = Gtk.FileFilter()
        scrivx_filter.set_name("Scrivener projects (*.scrivx)")
        scrivx_filter.add_pattern("*.scrivx")
        self.add_filter(filter=scrivx_filter)

        # É obrigatório utilizar ``show_all()``.
        self.show_all()

    def show_file_info(self):
        return self.get_filename()


def capitalizeFirstCharacter(name):
    p = ['da', 'de', 'di', 'do', 'du', 'para']  # preposição

    items = []
    for item in name.split():
        if not item in p:
            item = item.capitalize()
        items.append(item)

    return ' '.join(items)


def generate_unique_key(size=15):
    return secrets.token_urlsafe(size)[:size]


def generate_uuid():
    return str(uuid.uuid4())


class OutSaveFile(Gtk.Dialog):

    def __init__(self, parent, title):
        super().__init__(title="Salvar capivara?", transient_for=parent, flags=0)
        self.set_modal(modal=True)

        # Adicionando 1 botão.
        self.add_button(button_text='Cancelar', response_id=5000)
        # Adicionando mais de 1 botão.
        self.add_buttons(
            '_Não salvar', Gtk.ResponseType.NO,
            '_Salvar', Gtk.ResponseType.YES,
        )
        # Adicionando class action nos botões.
        btn_no = self.get_widget_for_response(
            response_id=Gtk.ResponseType.NO,
        )
        btn_yes = self.get_widget_for_response(
            response_id=Gtk.ResponseType.YES,
        )

        # Acessando o box.
        content_area = self.get_content_area()
        # configurando.
        content_area.set_halign(align=Gtk.Align.CENTER)
        content_area.set_border_width(border_width=12)
        content_area.set_spacing(spacing=6)

        label = Gtk.Label()

        label.set_markup(
            '<b>Salvar as alterações no documento "' + title + '" antes de fechar?\n\n</b>'
                                                               '<small>Suas alterações serão perdidas se não salvá-las.</small>'
        )

        content_area.add(widget=label)

        self.show_all()


class Date:

    def __init__(self):
        pass

    def stringToDate(strDate):
        return strDate[0:2] + '/' + strDate[2:4] + '/' + strDate[4:]

    def dateToString(strDate):
        day, month, year = strDate.split('/')
        return day + month + year

    def isValidDate(strDate):

        day, month, year = strDate.split('/')

        isValidDate = True
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            isValidDate = False

        finally:
            return isValidDate


class JsonTools():

    # CARREGAR O ARQUIVO JSON
    def __init__(self):
        pass

    def listSection(jsonFile, seccion, key, sort):
        lista = []
        for i in jsonFile[seccion]:
            lista.append(i[key])
        if sort:
            return sorted(lista)
        else:
            return lista

    def loadFile(file_name):
        logs = Logs(filename="capivara.log")

        logs.record("Carregando o arquivos json", type="info", colorize=True)

        # ler arquivo capivara
        try:
            with open(file_name, "r") as jsonFileLeitura:
                jsonFile = json.load(jsonFileLeitura)

        except IOError:
            logs.record("Arquivo : " + file_name + "inexistente.", type="info")
            raise CapivaraDoesNotExistError(10, "Arquivo %s inexistente" % file_name)

        except  ValueError:
            logs.record("Falha na decodificação do arquivo %s" % file_name)
            raise CapivaraDecodeFailError(20, "Falha ao decoficar o arquivo %s" % file_name)
            jsonFile = ""

        finally:
            pass

        return jsonFile

    def putObject(dataJson):
        return '{' + dataJson + '}'

    def putArray(dataJson):
        return '[' + dataJson + ']'

    def putMap(strKey, strValue):
        if not strValue:
            strValue = '""'
        return strKey + ' : ' + strValue

    def dict_from_str(dict_str):
        while True:
            try:
                dict_ = eval(dict_str)
            except NameError as e:
                key = e.message.split("'")[1]
                dict_str = dict_str.replace(key, "'{}'".format(key))
            else:
                return dict_


class AppConfig:
    # TODO: Incluir o tamanho da tela
    home = Path.home()
    config = configparser.ConfigParser(allow_no_value=True)
    # parse existing file
    config.read('capivara.ini')

    def __init__(self):
        self.DefaultWidth = int(self.get_ini_value("DEFAULT", "width"))
        self.DefaultHeight = int(self.get_ini_value("DEFAULT", "height"))
        self.myCapivaras = self.get_ini_value("DIRECTORY", "mycapivaras")
        self.lastFileOpen = self.get_ini_value("DIRECTORY", "last file open")
        self.darkMode = self.get_ini_value("PREFERENCES", "dark mode")
        self.updateAutomatically = self.get_ini_value("PREFERENCES", "update automatically")
        self.releases = self.get_ini_value("PREFERENCES", "releases")
        self.untestedReleases = self.get_ini_value("PREFERENCES", "untested releases")
        self.capivaraDirectory = self.get_ini_value("DIRECTORY", "mycapivaras")
        self.version = self.get_ini_value("CAPIVARA", "version")

    def setCapivaraVersion(self, value):
        self.version = value

    def getCapivaraVersion(self):
        return self.version

    def setCapivaraDirectory(self, value):
        self.capivaraDirectory = value

    def getCapivaraDirectory(self):
        return self.capivaraDirectory

    def setDefaultWidth(self, value):
        self.DefaultWidth = value

    def getDefaultWidth(self):
        return self.DefaultWidth

    def setDefaultHeight(self, value):
        self.DefaultHeight = value

    def getDefaultHeight(self):
        return self.DefaultHeight

    def setMycapivaras(self, value):
        self.myCapivaras = value

    def getMycapivaras(self):
        return self.myCapivaras

    def setLastFileOpen(self, value):
        self.lastFileOpen = value

    def getLastFileOpen(self):
        return self.lastFileOpen

    def getDarkmode(self):
        return self.darkMode

    def setDarkmode(self, value):
        self.darkMode = value

    def getUpdateAutomatically(self):
        return self.updateAutomatically

    def setUpdateAutomatically(self, value):
        self.updateAutomatically = value

    def getReleases(self):
        return self.releases

    def setReleases(self, value):
        self.releases = value

    def getUntestedReleases(self):
        return self.untestedReleases

    def setUntestedReleases(self, value):
        self.untestedReleases = value

    # Salva as variaveis globais na config
    def serialize(self):
        # DEFAULT
        self.set_ini_value('DEFAULT', 'width', self.DefaultWidth)
        self.set_ini_value('DEFAULT', 'height', self.DefaultHeight)
        self.set_ini_value('DEFAULT', 'last file open', self.lastFileOpen)

        # DIRECTORY
        self.set_ini_value('DIRECTORY', 'mycapivaras', self.capivaraDirectory)

        # PREFERENCES
        self.set_ini_value('PREFERENCES', 'dark mode', self.darkMode)
        self.set_ini_value('PREFERENCES', 'update automatically', self.updateAutomatically)
        self.set_ini_value('PREFERENCES', 'releases', self.releases)
        self.set_ini_value('PREFERENCES', 'untested releases', self.untestedReleases)

        cfgfile = open('capivara.ini', 'w')
        self.config.write(cfgfile)
        cfgfile.close()
        self.config.read('capivara.ini')

    # Carrega as configurações para variaveis globais
    def deserializer(self):
        pass

    def get_ini_value(self, section, key):
        return (self.config.get(section, key))

    def set_ini_value(self, section, key, value):
        if type(value) is int:
            value = str(value)
        self.config.set(section, key, value)


class DialogExportToPdf(Gtk.FileChooserDialog):
    # Definindo o diretório padrão.
    # home = Path.home()
    # home = Config.get_ini_value("DIRECTORY", "mycapivaras")
    home = "/Users/Elizeu/OneDrive - PRODESP/Documents/My Capivaras/"

    def __init__(self, name):
        super().__init__()

        fileName = name.capitalize()
        # dirname, basename = os.path.split(self.textbox.get_text())
        # self.chooser.set_current_name(basename)
        # self.chosser.set_current_folder(dirname)

        self.set_title(title='Salvar como')
        self.set_modal(modal=True)
        # Tipo de ação que o dialogo irá executar.
        self.set_action(action=Gtk.FileChooserAction.SAVE)
        # Nome inicial do arquivo.
        self.set_current_name(name=fileName)
        # Pasta onde o diálogo será aberto.
        self.set_current_folder(filename=str(self.home))
        # Adicionando confirmação de sobrescrita.
        self.set_do_overwrite_confirmation(do_overwrite_confirmation=True)

        # Botões que serão exibidos.
        self.add_buttons(
            '_Cancelar', Gtk.ResponseType.CANCEL,
            '_Salvar', Gtk.ResponseType.OK
        )

        pdfFilter = Gtk.FileFilter()
        pdfFilter.set_name("pdf")
        pdfFilter.add_mime_type("application/pdf")
        pdfFilter.add_pattern("*.pdf")
        self.add_filter(filter=pdfFilter)

        # É obrigatório utilizar ``show_all()``.
        self.show_all()

    def save_file(self):
        fileName = self.get_filename()
        fileName += "." + self.get_filter().get_name()
        # print(f'Caminho até o arquivo: {self.get_filename()}')
        # print(f'URI até o arquivo: {self.get_uri()}')
        return fileName


class DialogSaveRelationshipImage(Gtk.FileChooserDialog):
    # Definindo o diretório padrão.
    # home = Path.home()
    # home = Config.get_ini_value("DIRECTORY", "mycapivaras")
    home = "/Users/Elizeu/OneDrive - PRODESP/Documents/My Capivaras/"

    def __init__(self):
        super().__init__()

        fileName = 'Untitled'
        # dirname, basename = os.path.split(self.textbox.get_text())
        # self.chooser.set_current_name(basename)
        # self.chosser.set_current_folder(dirname)

        self.set_title(title='Salvar como')
        self.set_modal(modal=True)
        # Tipo de ação que o dialogo irá executar.
        self.set_action(action=Gtk.FileChooserAction.SAVE)
        # Nome inicial do arquivo.
        self.set_current_name(name=fileName)
        # Pasta onde o diálogo será aberto.
        self.set_current_folder(filename=str(self.home))
        # Adicionando confirmação de sobrescrita.
        self.set_do_overwrite_confirmation(do_overwrite_confirmation=True)

        # Botões que serão exibidos.
        self.add_buttons(
            '_Cancelar', Gtk.ResponseType.CANCEL,
            '_Salvar', Gtk.ResponseType.OK
        )

        # Criando e adicionando filtros.
        imgFilter = Gtk.FileFilter()
        imgFilter.set_name("png")
        imgFilter.add_mime_type("image/png")
        imgFilter.add_pattern("*.png")
        self.add_filter(filter=imgFilter)

        imgFilter = Gtk.FileFilter()
        imgFilter.set_name("jpg")
        imgFilter.add_mime_type("image/jpeg")
        imgFilter.add_pattern("*.jpg")
        self.add_filter(filter=imgFilter)

        pdfFilter = Gtk.FileFilter()
        pdfFilter.set_name("pdf")
        pdfFilter.add_mime_type("application/pdf")
        pdfFilter.add_pattern("*.pdf")
        self.add_filter(filter=pdfFilter)

        svgFilter = Gtk.FileFilter()
        svgFilter.set_name("svg")
        svgFilter.add_mime_type("image/svg+xml")
        svgFilter.add_pattern("*.svg")
        self.add_filter(filter=svgFilter)

        # É obrigatório utilizar ``show_all()``.
        self.show_all()

    def save_file(self):
        fileName = self.get_filename()
        fileName += "." + self.get_filter().get_name()
        # print(f'Caminho até o arquivo: {self.get_filename()}')
        # print(f'URI até o arquivo: {self.get_uri()}')
        return fileName


class DialogSaveFile(Gtk.FileChooserDialog):
    # Definindo o diretório padrão.
    # home = Path.home()
    # home = Config.get_ini_value("DIRECTORY", "mycapivaras")

    # TODO: Usar o caminho do próprio arquivo e o nome do arquivo original
    # TODO: Corrigir que está salvando com extensão .capivara.capivara

    # home = "/Users/Elizeu/OneDrive - PRODESP/Documents/My Capivaras/"

    def __init__(self):
        super().__init__()

        self.home = Global.config("my_capivara")
        self.capivaraFile = Global.config("title")

        if not Global.config("title"):
            self.capivaraFile = 'Untitled.capivara'
        else:
            fileOpen = Global.config("capivara_file_open")
            self.capivaraFile = self.capivaraFile  +  '.capivara'
            self.home = os.path.dirname(os.path.realpath(fileOpen))

        self.set_title(title='Salvar como')
        self.set_modal(modal=True)
        # Tipo de ação que o dialogo irá executar.
        self.set_action(action=Gtk.FileChooserAction.SAVE)
        # Nome inicial do arquivo.
        self.set_current_name(name=self.capivaraFile)
        # Pasta onde o diálogo será aberto.
        self.set_current_folder(filename=self.home)
        # Adicionando confirmação de sobrescrita.
        self.set_do_overwrite_confirmation(do_overwrite_confirmation=True)

        # Botões que serão exibidos.
        self.add_buttons(
            '_Cancelar', Gtk.ResponseType.CANCEL,
            '_Salvar', Gtk.ResponseType.OK
        )

        # Criando e adicionando filtros.
        txt_filter = Gtk.FileFilter()
        txt_filter.set_name(name='Capivara Files (*.capivara)')
        txt_filter.add_pattern(pattern='*.capivara')
        txt_filter.add_mime_type(mime_type='text/plain')
        self.add_filter(filter=txt_filter)

        all_filter = Gtk.FileFilter()
        all_filter.set_name(name='todos')
        all_filter.add_pattern(pattern='*')
        self.add_filter(filter=all_filter)

        # É obrigatório utilizar ``show_all()``.
        self.show_all()

    def save_file(self):
        return self.get_filename()


class DialogSelectImage(Gtk.FileChooserDialog):
    # Definindo o diretório padrão.
    home = Path.home()

    def __init__(self, select_multiple):
        super().__init__()
        self.select_multiple = select_multiple

        self.set_title(title='Abrir')
        self.set_modal(modal=True)

        #
        # Tipo de ação que o dialogo irá executar.
        self.set_action(action=Gtk.FileChooserAction.OPEN)

        # Defininido se a seleção será multipla ou não
        self.set_select_multiple(select_multiple=self.select_multiple)
        # Pasta onde o diálogo será aberto.
        self.set_current_folder(filename=str(self.home))

        # Botões que serão exibidos.
        self.add_buttons(
            '_Cancelar', Gtk.ResponseType.CANCEL,
            '_OK', Gtk.ResponseType.OK
        )

        # Adicionando class action nos botões.
        # btn_cancel = self.get_widget_for_response(
        #     response_id=Gtk.ResponseType.CANCEL,
        # )
        # btn_cancel.get_style_context().add_class(class_name='destructive-action')
        #
        # btn_save = self.get_widget_for_response(
        #     response_id=Gtk.ResponseType.OK,
        # )
        # btn_save.get_style_context().add_class(class_name='suggested-action')

        # Criando e adicionando filtros.
        img_filter = Gtk.FileFilter()
        img_filter.set_name("Image files")
        img_filter.add_pattern("*.jpg")
        img_filter.add_pattern("*.jpeg")
        img_filter.add_pattern("*.png")
        img_filter.add_pattern("*.tif")
        img_filter.add_pattern("*.bmp")
        img_filter.add_pattern("*.gif")
        img_filter.add_pattern("*.tiff")
        self.add_filter(filter=img_filter)

        all_filter = Gtk.FileFilter()
        all_filter.set_name(name='todos')
        all_filter.add_pattern(pattern='*')
        self.add_filter(filter=all_filter)

        # É obrigatório utilizar ``show_all()``.
        self.show_all()

    def show_file_info(self):
        return self.get_filename()


class DialogSelectFile(Gtk.FileChooserDialog):

    # Definindo o diretório padrão.
    appConfig = AppConfig()

    home = os.path.dirname(os.path.realpath(appConfig.getLastFileOpen()))

    if not home:
        home = appConfig.getCapivaraDirectory()

    def __init__(self, select_multiple):
        super().__init__()
        self.select_multiple = select_multiple

        self.set_title(title='Abrir Capivara')
        self.set_modal(modal=True)

        #
        # Tipo de ação que o dialogo irá executar.
        self.set_action(action=Gtk.FileChooserAction.OPEN)

        # Defininido se a seleção será multipla ou não
        self.set_select_multiple(select_multiple=self.select_multiple)
        # Pasta onde o diálogo será aberto.
        self.set_current_folder(filename=str(self.home))

        # Botões que serão exibidos.
        self.add_buttons(
            '_Cancelar', Gtk.ResponseType.CANCEL,
            '_OK', Gtk.ResponseType.OK
        )

        # Adicionando class action nos botões.
        # btn_cancel = self.get_widget_for_response(
        #     response_id=Gtk.ResponseType.CANCEL,
        # )
        # btn_cancel.get_style_context().add_class(class_name='destructive-action')
        #
        # btn_save = self.get_widget_for_response(
        #     response_id=Gtk.ResponseType.OK,
        # )
        # btn_save.get_style_context().add_class(class_name='suggested-action')

        # Criando e adicionando filtros.
        txt_filter = Gtk.FileFilter()
        txt_filter.set_name(name='Capivara Files (*.capivara)')
        txt_filter.add_pattern(pattern='*.capivara')
        # txt_filter.add_mime_type(mime_type='text/plain')
        self.add_filter(filter=txt_filter)

        all_filter = Gtk.FileFilter()
        all_filter.set_name(name='todos')
        all_filter.add_pattern(pattern='*')
        self.add_filter(filter=all_filter)

        # É obrigatório utilizar ``show_all()``.
        self.show_all()

    def show_file_info(self):
        return self.get_filename()


class DialogUpdateAutomatically(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Capivara update", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_NO, Gtk.ResponseType.CANCEL, Gtk.STOCK_YES, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)
        label1 = Gtk.Label(label="")
        label2 = Gtk.Label(label="An update package is available, do you want to download it?")
        label3 = Gtk.Label(label="")

        box = self.get_content_area()
        box.add(label1)
        box.add(label2)
        box.add(label3)
        self.show_all()


def getPlugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = importlib.find_module(MainModule, [location])
        plugins.append({"name": i, "info": info})
    return plugins


def loadPlugin(plugin):
    return importlib.import_module(plugin, PluginFolder)


def alert(widget, message):
    dialog = Gtk.MessageDialog(widget, 0, Gtk.MessageType.ERROR,
                               Gtk.ButtonsType.CANCEL, "Error")
    dialog.format_secondary_text(message)
    dialog.run()
    print("INFO dialog closed")

    dialog.destroy()


def imageToBase64(widget, imageFile):
    base64_string = ""
    try:
        with open(imageFile, "rb") as img_file:
            base64_string = base64.b64encode(img_file.read())
    except IOError:
        alert(widget, "Erro ao tentar abrir o arquivo de imagem")

    finally:
        img_file.close()

    return base64_string


def base64ToImage(widget, base64_string):
    try:
        imgdata = base64.b64decode(base64_string)
    except:
        alert(widget, "Erro ao abrir a imagem")
    finally:
        imgdata = ""

    return imgdata


def get_pixbuf_from_base64string(base64string):
    if base64string is None:
        return 'NOIMAGE'
    raw_data = base64.b64decode(base64string)
    try:
        pixbuf_loader = GdkPixbuf.PixbufLoader.new_with_mime_type("image/jpeg")
        pixbuf_loader.write(raw_data)
        pixbuf_loader.close()
        pixbuf = pixbuf_loader.get_pixbuf()
        return pixbuf
    except Exception as e:
        pass
    try:
        pixbuf_loader = GdkPixbuf.PixbufLoader.new_with_mime_type("image/png")
        pixbuf_loader.write(raw_data)
        pixbuf_loader.close()
        pixbuf = pixbuf_loader.get_pixbuf()
        return pixbuf
    except Exception as e:
        pass
    return ""

