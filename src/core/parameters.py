from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import os
import codecs
import math

class Parameters():
    def __init__(self, app_directory):
        self.app_directory = app_directory
        self.param_dir = "~/.chemyxconnector"
        self.param_file = "~/.chemyxconnector/parameters.txt"
        self.library_file = "~/.chemyxconnector/library.txt"
        if os.path.exists(os.path.expanduser(self.param_dir)):
            if os.path.isfile(os.path.expanduser(self.param_file)):
                self.readPreferences()

    def setDefaultParams(self):
        pass

    def resetParameters(self):
        pass

    def readParameters(self):
        pass

    def writeParameters(self):
        pass