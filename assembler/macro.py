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

    def getVaryForArg(self, args):
        for v in self.varies:
            if len(args) == len(v.args):
                index = 0
                for a in args:
                    if vals.getType(a) != v.args[index][0]:
                        continue
                    index+=1
                return v
        return False

class MacroVariation:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

    #Apply args to body
    def applyArgs(self, args):
        argNames = []
        body = self.body
        for a in self.args:
            argNames.append(a[1])
        argVals = args
        for a in argNames:
            index = 0
            loc = self.body.find
