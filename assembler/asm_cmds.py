#Macro commands are effectivley macros programmed in python
import vals
import assemble
from util import *

class MacroCmdBase:
    #Args are a list of args the macro is called with
    def __init__(self, args):
        self.args = args
        self.types = []
        self.genTypes()
        self.asm = ""
        self.setName()
        self.asm += self.name
        for i in self.args:
            self.asm += " " + i
        self.asm += ";"

    def genTypes(self):
        for a in self.args:
            self.types.append(vals.getType(a))

    def setName(self):
        self.name = "base"

    def checkArgs(self):
        #If an error occurs, print a message here
        return True

    #Return tokens to add in to the code
    def getResult():
        return []

class call(MacroCmdBase):
    def setName(self):
        self.name = "call"

    def checkArgs(self):
        if len(self.args) < 1:
            error("call takes at least one argument", self.asm)
        if self.types[0] != vals.TYPE_MEM:
            error("the first argument to call has to be a memory location", self.asm)
        return True

    def getResult():
        cmd = self.args[0]
        asm = "";


a = call(["func"])
a.checkArgs()
