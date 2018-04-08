from util import *
import vals
#For macro ids
import uuid
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
        #put arg names and passed args in argNames and argVals
        argNames = []
        body = self.body
        for a in self.args:
            argNames.append(a[1])
        argVals = args
        for i in range(len(argVals)):
            if argVals[i][0] == '{' and argVals[i][-1] == '}':
                argVals[i] = argVals[i][1:-1]
        #Add MACROID's to argNames and argVals (16 MACROID's)
        for n in range(16):
            argNames.append("MACROID" + hex(n)[2:].upper())
            argVals.append(uuid.uuid4().hex.upper())

        argIndex = 0
        for a in argNames:
            loc = body.find(a)
            while loc != -1:
                endIndex = loc + len(a)
                if (loc == 0 or body[loc-1] in vals.SEPARATORS) and (endIndex >= len(body) or body[endIndex] in vals.SEPARATORS):
                    body = body[:loc] + argVals[argIndex] + body[endIndex:]
                #Even with replacing of argNames, loc is still the place to begin searching to not get stuck in loops with args inside text
                loc = body.find(a, loc + 1)
            argIndex += 1
        return body
