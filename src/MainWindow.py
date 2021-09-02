# -*- coding: utf-8 -*-
"""Capivara"""

import gi

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gio, Gtk, GdkPixbuf, GLib


import Global
from Global import Global
from Utils import AppConfig, DialogUpdateAutomatically, DialogSelectFile, DialogSaveFile, DialogSelectImage, Treeview
import PluginsManager
import webbrowser
from CapivaraSmartGroup import CapivaraSmartGroup
from DataAccess import DataUtils, ProjectProperties, Character, Core, SmartGroup
import Utils
from src.logger import Logs

# importar Telas
from Preferences import Preferences
from ProjectPropertiesDialog import ProjectPropertiesDialog
from NewGroupDialog import NewGroupDialog
from PluginsManager import PluginsManager

logs = Logs(filename="capivara.log")


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
    imgCharacter = Gtk.Template.Child(name='imgCharacter')


    # Obtendo as configurações
    appConfig = AppConfig()

    if appConfig.getDarkmode() == 'yes':
        settings.set_property('gtk-application-prefer-dark-theme', True)
    else:
        settings.set_property('gtk-application-prefer-dark-theme', False)

    logo = GdkPixbuf.Pixbuf.new_from_file(filename='assets/icons/icon.png')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # IMAGEM INICIAL DO PERSONAGEM
        __NOIMAGE = '''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oooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAK2oX1vpmnXN/dyBLe2iaWRj2VRk/wAq+SPiV8SNQ8a6ttAe302E5t7Y+n95vViP0r1b9oLxcNP0S28N28uJ70iW4CnkRKflB+rDP/AfevmtmLMSepoATqaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDrfAnjnU/BetpeWLGRHwlxbM2EuE9D6MOzDkE9wSD9e+HdfsfE+g2usaezG3uV3BXGGQg4KsPUEEV8K17t+zx4uEOo3Xhe5k+W6BuLYH/noo+cD6qAf+AH1oA+iaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKrahfW+l6bdaheSeXbWsTzTPgnaigknA5PA7VZrzb4465/ZHw3urZH2zai62y4PO37zfouP8AgVAHzN4x8S3Hi7xVfazcZAnkPlIf+WcY4VfwGPxzWFRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABV/RNTudG1q01KzcJc20qyxsem4HIz6jjBHeqFFAH3Z4e1u28R+H7HWLQ/ubuISBc5KHoyn3BBB9xWnXjP7O+ufa/DGoaPI2Xs51mTJ/gkHIA9mUn/gVezUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAV82ftGa8bjxLp2ixP8lnAZJB/tydv++VB/wCBV9J18S+P9YfXfHWsXzMWV7pxGc5+QHao/wC+QKAOaooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA9N+BuvDSfiLZ2zuI4r6N7V8ngk/Mn47lUfjX1lXwZpWoS6VqltfwErNbyrLG3oysGB/MV912V3Ff2FveQHMVxEsqH1VgCP0NAFiiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAyfE2pDR/C+q6iW2m2tZJFP+0FOP1xXwxISZXJOSWO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zAa1fqdhB5gi5Bk+uRhffJ/hwfk+gAooooAKKKKACiiigAooooAKKKKACiiigArt/hFp51H4oaJGBlY5vPJ9NgL/APstcRXsf7O1ibnxpd3bZKWlo5X2Zyq/yDflQB9OUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB5l8eNKOpfDOeZRlrG4iuBgc4zsP4fPn8K+Ta+5/FeknXfCWraWqgvc2skcef7+07T/31ivhuUETOGBBDHIPWgBlFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH2h8LNMXSfhh4et1cv5lotySfWXMuPw34/Cul1LULfStMu9Ru3KW1rC88rAZIRQSeO/AqS0tYLGygs7aNY7eCNYokUYCqowAPoBXmfx+1l9L+Gz2kRAfUbmO3bDYIQZdiPX7gU+zUAfNXinxHe+LPEd5rN87GS4kJRC2REn8KDpwBx79epNY9FFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABX0r+znpgi8OarqmwL9onSAf8ATJP4mT9K+aq+yfhNpLaR8NdIjljKTTo1zJnqd7FlP8A3ztoA7aiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvj/4w+G/+Ed+IOoBI9lvdv9qgwMAq+S35MGH4V9gV5N8fPDEer+Cl1iNP9K0twcgdYnIVh+B2n2Ab1oA+WaKKKACiiigAooooAKKKKACiiigAooooAK2/BkEd1458P28q7o5dStkceoMqg1iVr+FL630vxjoeoXb+XbWuoQTzPtJ2osisxwOTwD0oA+6K+d/2l72F9R8O2KsPPhinmdfRXKBT+cbflXpH/C7fh5/0MP8A5JXH/wAbrwf41eKtG8XeM7W/0O7N1axWCQNIYmT5xJIxGGAPRh2oA84ooooAKKKKACiiigAooooAKKKKACiiigAooooA3/BXh+TxR4w03SIwcTzDzCP4UHLH8FBr7dijSGJIo1CRooVVA4AHQV4R+zp4WRLfUPE86ZlZvslvkfdAwXP45Ufga96oAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKxvFiW8ng7W0uhm3NjP5g/2dhzj3rZrlfiSzr8N/EBj6/Y3B+h6/pmgD4qooooAKKKKACiiigAooooAKKKKACiiigAorS0DQ77xLrtpo+mxh7u6fYgY4A4yWJ9AASfYV9c+B/hloHgiyi+z28d1qQX97fzIDIzd9vXYvsPxJPNAHxpRX3/VLVNI03W7NrTVLG3vLdusc8YcfUZ6H3FAHwbRXpvxc+F3/CC3seo6azSaHdybIw5y9vJgnyyf4gQCVPXAIPIy3mVABRRRQAUUUUAFFFFABRRRQAUUUUAFKpwwPoaSigD7G+D6W6/CzRGtgNrpIzH1bzG3fqP0rua80+BMkj/C+0DklVnlCZ7DOePxJr0ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArn/HUZl8AeIkAyf7NuCPwjY10FRXNvDd2sttcRrJDMhjkRujKRgg/hQB8C9Dg0+SJo8bu9e/XX7Okkmvu1tq0MelGTcrOC0yp/d24Ckjn5s+nFcJ8aPD1v4b8aQWVpHstzYQGP1IVfLyff5KAPOaKKKACiiigAooooAKKKKACiiigD2/8AZs0qOfxBreqsfntLaOBFI/56sST9f3WPxNfSFfOv7NN/BHqviHTmJ8+eCGdBjjbGzK36yrX0VQAUUUUAcn8TtNg1X4Z+IYJx8sdlJcKR1DRDzF/VRXxZX2x8RryCx+G3iSW4cIjadNECf7zoUUfizAfjXxPQAUUUUAFFFFABRRRQAUUUUAFFFFAD4VV540YsFZgCVGTjPYU0jBIPauu+FumrqvxL0K2aMSKLkSsrAEEIC5yD7LXqWofs6ynXN+n6tENNZw375T5sS55GAMMQOhyPpQB3/wAFofJ+Feknj940z4Hb96w/pXf1n6Jo9n4f0W10mwQpa2ybEBOSe5J9yST+NaFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAV86ftLWqJq/h+7AG+WCaMnvhWUj/0M19F18/ftMgbvC7dyLof+iaAPAaKKKACiiigAooooAKKKKACiiigDc8IeKLzwd4ntNbshveAkSRFiFlQjDKfqOnXBAPavsfwr4u0bxjpEeo6RdCRSB5kLYEkLf3XXsf0PYkV8OVZsdQvdMulutPvLi0uFGBLbytG4/EEGgD72prukUbSSMqIoLMzHAAHUk18Rf8J34w/6GvXP/BjN/wDFVU1DxPr+r2/2fUtc1O9gzny7m7kkXPrhiRQB6f8AGv4pW3iZl8OaFKZNMt5Q9xdKxC3Eg6Kvqg65PU4I4AJ8boooAKKKKACiiigAooooAKKKKACiiigD1T9n62Sf4lrK3WCzldfqcL/JjX1XXzJ+zjEreONQkIyV05wPb95HX03QAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABXz/+01/zK/8A29/+0a+gK8p/aA01rz4ex3KDDWl4js2OisGQ/hlloA+VqKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAPbf2blB8T6u+ORZ4z9XX/CvpKvBf2atOxZa9qbL96SKBG+gLN/Na96oAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArlfiTp39qfDjXrULuItGlCjuY8OP1WuqqK5gjuraW3lXdHKhRx6gjBoA+CJWLTOzHJLEk0yrWpWM2mapd2FwMT20zQyD0ZSQf1FVaACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKOpop0f+sX6igD61+Bunmy+GtvOVAa9uJZ+BjjOwf8AoFekVh+DdMOjeDNG09l2vBaRq4x/HtBb9Sa3KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAPmL4/+Ev7L8VRa9bRkW+ppmXHQTKAD9MrtPud1eO19p/EjwsPF/ge/01EDXSr59qe4lXoB9Rlf+BV8WsjIxV1KsOoIwaAEooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvQfg54U/4Sfx7ameLfZWP+lT7hkHaflX3y2PwzXn4G5gB34r60+CfhU+HvA0V5cR7b3U8TuT1EeP3Y/L5v+BUAelUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFfMPxu+HL6FrL+ItOjJ02+cmVVH+omJyR7K2SR6HI44z9PVS1XS7PWtKudM1CFZrS5jMciHuD3HoR1B7EA0AfBtFa/inSl0LxPqWlI5dLO5kgVyMFgrEAn3IFZFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABQASQAMk9AKKmtFL3caKcFjjP1oA7z4U/Dybxr4j33UbppNmwa6cjG89ox7nv6D8K+uo40ijSKNQqIAqqOgA6Csjwr4asfCXh+20mwX5Ihl5CPmlc9WPuf06VtUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB8T/Eb/ko3iH/sIT/+jGrmK6f4jf8AJRvEP/YQn/8ARjVzFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABViwOL+A+jiq9T2X/H7D/vCgD74ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACsnxNrkPhvw3qGsTgMtrCXCk43t0VfxJA/Gtavmz47/EUapfP4R03H2S0lDXc4bPmygfcXH8K55z1YdsZIB49qd5NqGozXdxIZJ5nMkjnuxJJ/nVSiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAp8JAlBJwKZRQB9ofDTxOfFngawv5H3XcQ+z3XOT5iYGT7kbW/wCBV19fKfwW+IUXhHXZdN1N9ul6gVDSk8QSDhWP+zzg/ge1fVY56UALRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRXHfELx9YeBNEaeUrLqEwItbbPLH+83oo/XpQBzvxh+JC+FNLbSNNmH9r3cZy6nm3jPG7/ePb8/SvlWSRpZGdiSSc5Jq7rGr3mualPqF/M01zO5eR26k/0HtVCgAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAFRijBh2r6O+CPxKF7BF4V1ef9/GuNPmc/fUf8sj7j+H1HHYZ+cKmtbqa0nSaCR45I2Do6MVZWHIII6EHvQB980V5z8KviXB420pLO9kVNbt4/3q4C+eo48xR0+oHQ+1ejUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRWF4s8Vad4P0OXVNRf5V4iiU/NM/ZV/x7UAVvG3jXTfBGhvf3zb5mytvbqfmlf09h6mvj3xL4k1HxVrc+q6nOZJ5TwP4UXsqjsBVzxl4x1Lxlrkuo6hJkn5Y4lPyRJ2VR6e/c1zlABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQBe0jVrvRtRgvrGd4LmBxJFKnVGH8x6g9RX1x8NviNZ+PNI+bZBq1uo+1W4PB7eYnfaT+Kng9ifjmtPQNev/DerQalps7Q3MDblZe/qCO4PQigD7sorkvAHjyw8d6ELu32xXkIC3dtnJjY9x6qcHB/DqDXW0AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAYXjDxLD4Q8Kahr09vJcJaIpEKEAuzMEUZPQbmGTzgZOD0Px74r8aa74z1H7ZrN4ZNuRFDGNkcSkk7VUfXGTkkAZJxRRQBz9FFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAbXhbxRqXhDXrfV9Ml2SxHDofuSoeqMO4OP0BHIFfZnhfxDb+KfDtrq9tFJCswO6KUfNG4OGU+vI69xRRQBs0UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH/2Q=='''
        pixbuf = Utils.get_pixbuf_from_base64string(__NOIMAGE)
        pixbuf = pixbuf.scale_simple(170, 200, 2)
        self.imgCharacter.set_from_pixbuf(pixbuf)

        self.context_id = self.statusbar.get_context_id(
            context_description='exemplo',
        )

        self.statusbar_show_msg("Teste")

        # NOVA VERSÃO
        # TODO: Verificar se existe nova versão e apresentar no Info
        newVersion = True
        if not self.info_bar.get_revealed() and newVersion:
            self.info_bar.set_revealed(revealed=True)
            GLib.timeout_add_seconds(priority=0, interval=5, function=self.info_bar_timeout)

        # # Verifica se existe nova versão disponível
        # if self.appConfig.getUpdateAutomatically() == "yes":
        #     # TODO: Criar função para verificar se existe nova versão disponível
        #     newVersion = True
        #     if newVersion:
        #         dialog = DialogUpdateAutomatically(self)
        #         response = dialog.run()
        #         if response == Gtk.ResponseType.OK:
        #             print("The OK button was clicked")
        #         elif response == Gtk.ResponseType.CANCEL:
        #             print("The Cancel button was clicked")
        #
        #         dialog.destroy()

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
        capivara = dataUtils.LoadCapivaraFileEmpty(propertiesProject)

        Biografia_Character = [
            (1965, 'Nascimento'), (1974, 'Evento 1'), (1976, 'Evento 2'), (1979, 'Evento 3'),
            (1980, 'Evento 4'), (1985, 'Evento 5'), (1987, 'Evento 6'),
        ]

        for state in Biografia_Character:
            self.list_store.append(row=state)

            self.show_all()

        Treeview(self.treeView, capivara)

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
            strTeste64 = '''/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB
AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEB
AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAHzAYoDASIA
AhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA
AAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3
ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm
p6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA
AwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx
BhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK
U1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3
uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD+6CGb
zpf9R7f8fg7cj8unv3ommgz/AK/jj6/56n+vaq8Hf8f6VY8j3/X/AOtQc5Ym/ffZ/bv9s7f/AFgf
171Xm8jzf5/6Z/k/j1FH7r/O2jzoPKuPf+n0x/Kj6t5fh/8AanQE32eD7P8AuPp/pnb1+v8AX6ZF
n/R/+eB/8C//AK1VvO838Pb/AD0z7dfyrzTed+447n09Px7/AONH1Xy/D/7UCvew/wDPf3z/AKZ+
f+T7Yrn5ofJi/cQW32gD7F9k4/tP09x+nfHrXQYnm/1//Hx6evP1H5+2fp8v/tFfFqfwr4N1jSvA
89tc+ONUszotnd2d5j+wf7d/5jXY+3GM/rXLipLBq91p7yu/+D/W1rhhcN9caXd9fx8+vl99kePf
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
f+3TlNM/5dv+vM/0oooryz6c/9k='''

            pixbuf = Utils.get_pixbuf_from_base64string(stringBase64)
            pixbuf = pixbuf.scale_simple(170, 200, 2)
            self.imgCharacter.set_from_pixbuf(pixbuf)


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
            fileOpen = dialog.show_file_info()
            dataUtils = DataUtils()
            capivara = dataUtils.loadCapivaraFile(fileOpen)

            if not capivara:
                dialog.destroy()
                dlgMessage = Gtk.MessageDialog(
                    transient_for=self,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text="ERROR",
                )
                dlgMessage.format_secondary_text("Não foi possível carregar o arquivo.")
                dlgMessage.run()

                dlgMessage.destroy()
            else:
                Treeview(self.treeView, capivara)

                projectProperties = ProjectProperties.get()
                self.header_bar.set_title(projectProperties.title)
                self.header_bar.set_subtitle(projectProperties.surname + ', ' + projectProperties.forename)

                # Destruindo a janela de dialogo.
                dialog.destroy()

        elif response == Gtk.ResponseType.NO:
            pass

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
        appConfig = AppConfig()

        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)

        win.set_title("Untitled")
        win.set_default_size(width=appConfig.getDefaultWidth(), height=appConfig.getDefaultHeight())
        win.set_position(position=Gtk.WindowPosition.CENTER)
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

# if __name__ == '__main__':
#     import sys
#
#     app = Application()
#     app.run(sys.argv)
