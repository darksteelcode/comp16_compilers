from util import *
import vals
'''
Macro functions - this file contains the macro class, and tools to apply macro commands
'''

class Macro:
    def __init__(self, name):
        self.name = name
        #Contains each macro variation for the macro
        self.varies = []

    def addVariation(self, vary):
        self.varies.append(vary)

class MacroVariation:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body
