# -*- coding: utf-8 -*-
__author__ = 'ChenMei'

import ConfigParser

class Util:
    @staticmethod
    def getConfig(file, section, key):
        config = ConfigParser.ConfigParser()
        config.read(file)
        return config.get(section, key)