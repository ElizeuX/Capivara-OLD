# -*- coding: utf-8 -*-

import sys
from MainWindow import Application
from SplashScreen import Splash
from src.logger import Logs
import gettext
import locale
from os.path import join as path_join


from time import sleep

# def init_locale():
#     locale.setlocale(locale.LC_ALL, )
#     (loc, enc) = locale.getlocale()
#
#     filename = path_join('lang', '{}.{}',
#                          'LC_MESSAGES/messages.mo').format(loc)
#     try:
#         trans = gettext.GNUTranslations(open(filename, "rb"))
#     except IOError:
#         trans = gettext.NullTranslations()
#
#     trans.install()


logs = Logs(filename="capivara.log")

# Initiate and show the splash screen
logs.record("Starting splash", type="info", colorize=True)

splash = Splash()
splash.start()

# CONFIGURANDO O APLICATIVO
# logs.record("configurando plugins", type="info", colorize=True)
# plugin = Utils.loadPlugin("__init__")
# plugin.run()

sleep(1)

#init_locale()

# Destroy splash
splash.destroy()

app = Application()
print(sys.argv)
app.run(sys.argv)
