# -*- coding: utf-8 -*-

import sys
from MainWindow import Application
from SplashScreen import Splash
import Utils
import logging

from time import sleep

logging.basicConfig(level=logging.INFO)

# Initiate and show the splash screen
logging.info("Starting splash")

splash = Splash()
splash.start()

# CONFIGURANDO O APLICATIVO
logging.info("configurando plugins")
plugin = Utils.loadPlugin("__init__")
plugin.run()


sleep(1)

# Destroy splash
splash.destroy()

app = Application()
app.run(sys.argv)
