# -*- coding: utf-8 -*-

import sys
from MainWindow import Application
from SplashScreen import Splash
import Utils
from src.logger import Logs

from time import sleep

logs = Logs(filename="capivara.log")

# Initiate and show the splash screen
logs.record("Starting splash", type="info", colorize=True)

splash = Splash()
splash.start()

# CONFIGURANDO O APLICATIVO
logs.record("configurando plugins", type="info", colorize=True)
plugin = Utils.loadPlugin("__init__")
plugin.run()

sleep(1)

# Destroy splash
splash.destroy()

app = Application()
print(sys.argv)
app.run(sys.argv)
