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

    def getVaryForArgs(self, args):
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
        for i in range(len(argVals)):
            if argVals[i][0] == '{' and argVals[i][-1] == '}':
                argVals[i] = argVals[i][1:-1]
        argIndex = 0
        for a in argNames:
            loc = body.find(a)
            while loc != -1:
                endIndex = loc + len(a)
                print body[loc:endIndex]
                if (loc == 0 or body[loc-1] in vals.SEPARATORS) and (endIndex >= len(body) or body[endIndex] in vals.SEPARATORS):
                    body = body[:loc] + argVals[argIndex] + body[endIndex:]
                loc = body.find(a)
            argIndex += 1
        return body
