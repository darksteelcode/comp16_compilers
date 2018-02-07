import vals
from util import *

#cmd is of Cmd class, out is file to write to
#base is a generic class tailored to be parent for basic asm commands
class base:
    def __init__(self, cmd, out):
        self.cmd = cmd
        self.out = out
        #Compiler
        self.com = None
        #Default
        self.LENGTH = 1
        self.initVars()
        self.checkVars()

    def initVars(self):
        #lens in array of len of each argument that will be written in bits - does not include opcode
        self.lens = []
        #types is array of types for each args
        self.types = []
        #length of cmd in number of commands (1 for a signle asm command)
        self.LENGTH = 0

    def checkVars(self):
        if len(self.lens) != len(self.cmd.args):
            error(self.cmd.cmd + " passed " + str(len(self.cmd.args)) + " arguments, but it requires " + str(len(self.lens)), self.cmd.toAsm())
        argI = 0
        for t in self.types:
            if t != self.cmd.types[argI]:
                error("Argument number " + str(argI) + " to " + self.cmd.cmd + " is " + vals.typeToName(self.cmd.types[argI]) + ", but should be " + vals.typeToName(t), self.cmd.toAsm())
            argI += 1

    def assignCompiler(self, com):
        self.com = com

    def getMemDefines(self):
        #Returns a list of defined memory locatiosn, in the format of [[name, offset from begining of command], ...]
        #For eaxmple, if the cmd defines "start" as the first location in the command, and "end" as the fourth location, this would return the folowing:
        #[["start", 0], ["end", 3]]
        return []

    def emit(self):
        #This is where self.out would be written to
        lenI = 0
        for i in self.cmd.args
            print i
            lenI += 1
        pass
