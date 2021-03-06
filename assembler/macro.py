from util import *
import vals
#For macro ids
import uuid
import assemble
'''
Macro functions - this file contains the macro class, and tools to apply macro commands
'''

def applyMacrosToTokens(tokens, macros):
    #tokens with macros applied
    finalTokens = []
    #Apply macros here
    for t in range(len(tokens)):
        appliedMacro = False
        for m in macros:
            if tokens[t].cmd == m.name:
                body = m.applyArgs(tokens[t].args)
                replaceTokens = assemble.asmToCompilerRdyTokens(body)
                finalTokens = finalTokens + replaceTokens
                appliedMacro = True
                break
        if not appliedMacro:
            finalTokens.append(tokens[t])
    return finalTokens

class Macro:
    def __init__(self, name):
        self.name = name
        #Contains each macro variation for the macro
        self.varies = []

    def addVariation(self, vary):
        self.varies.append(vary)

    def getVaryForArgs(self, args):
        for v in self.varies:
            good = True
            if len(args) == len(v.args):
                index = 0
                for a in args:
                    if vals.getType(a) != v.args[index][0]:
                        #Don't allow ANY when code is passed
                        if v.args[index][0] != vals.TYPE_ANY or vals.getType(a) == vals.TYPE_CODE:
                            good = False
                    index+=1
            else:
                good = False
            if good:
                return v
        return False

    def applyArgs(self, args):
        vary = self.getVaryForArgs(args)
        if vary:
            return vary.applyArgs(args)
        else:
            error("No acceptable macro variation found for macro " + str(self.name) + " with arguments " + " ".join(args), "#macro " + self.name)

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
                if (loc == 0 or body[loc-1] in vals.MACRO_NAME_SEPERATORS) and (endIndex >= len(body) or body[endIndex] in vals.MACRO_NAME_SEPERATORS):
                    body = body[:loc] + argVals[argIndex] + body[endIndex:]
                #Even with replacing of argNames, loc is still the place to begin searching to not get stuck in loops with args inside text
                loc = body.find(a, loc + 1)
            argIndex += 1
        return body
