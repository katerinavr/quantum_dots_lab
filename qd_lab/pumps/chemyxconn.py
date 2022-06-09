#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore

import sys
import os
import time
import inspect

from core import parameters
from gui import mainscreen

def get_script_dir(follow_symlinks = True):
    if getattr(sys, 'frozen', False):
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

def startGUI(params_object):
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    
    #app = QApplication(sys.argv)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app.setStyle('Fusion')
    resources_path = os.path.abspath(os.path.join(params_object.app_directory, 'static'))
    # splash_pix = QPixmap(os.path.join(resources_path, 'logo-with-tagline@500px.png'))
    # splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    # splash.show()
    # time.sleep(2)
    window = mainscreen.MainWindow(__VERSION__, params_object, resources_path)
    window.show()
    # splash.finish(window)
    sys.exit(app.exec_())

   
script_dir = get_script_dir()
os.chdir(script_dir)
#__VERSION__ = open('VERSION', 'rU').read()
__VERSION__ = open('VERSION', 'r').read()
params = parameters.Parameters(script_dir)
startGUI(params)