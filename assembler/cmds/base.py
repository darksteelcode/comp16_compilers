import vals
from util import *

#cmd is of Cmd class, out is file to write to
#base is a generic class tailored to be parent for basic asm commands
class base:
    def __init__(self, cmd, out):
        #Number of optional argumentrs at the end of the cmd
        self.opts = 0
        self.cmd = cmd
        self.out = out
        #Compiler
        self.com = None
        #Default
        self.LENGTH = 1
        self.vals = []
        self.lens = []
        self.types = []
        self.initVars()
        self.checkVars()

    def initVars(self):
        #self.vals is array of int vals to emit - should be init'ed to include opcode
        self.vals = []
        #lens in array of len of each argument that will be written in bits - includes opcode
        self.lens = []
        #types is array of types for each args - does't include opcode
        self.types = []
        #length of cmd in number of commands (1 for a signle asm command)
        self.LENGTH = 0
        #Number of optional arguments at the end of the command
        self.opts = 0

    def checkVars(self):
        missing = (len(self.lens) - len(self.vals)) - len(self.cmd.args)
        if missing != 0:
            if missing <= self.opts and missing >= 0:
                for i in range(missing):
                    self.cmd.args.append("0")
                    self.cmd.types.append(vals.TYPE_VAL)
            else:
                error(self.cmd.cmd + " passed " + str(len(self.cmd.args)) + " arguments, but it requires " + str(len(self.lens)-len(self.vals)), self.cmd.toAsm())
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

    def convToValues(self):
        for i in self.cmd.args:
            self.vals.append(self.com.getValue(i))

    def handleSpecialVals(self):
        pass

    def emit(self):
        #This is where self.out would be written to
        self.convToValues()
        self.handleSpecialVals()
        if len(self.vals) == len(self.lens):
            out = intsToCmd(self.vals, self.lens)
            self.out.write(out)
            self.out.flush()
        pass
