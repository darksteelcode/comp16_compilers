import vals
from util import *

#cmd is of Cmd class, out is file to write to
class base:
    def __init__(cmd, out):
        self.cmd = cmd
        self.out = out
        #VariableResolver
        self.var = None
        #Default
        self.LENGTH = 1
        self.initVars()

    def initVars(self):
        #lens in array of len of each argument
        self.lens = []
        #types is array of types for each args
        self.types = []
        #length of cmd in number of commands (1 for a signle asm command)
        self.LENGTH = 0

    def assignVariableResovler(self, var):
        self.var = var

    def getMemDefines(self):
        #Returns a list of defined memory locatiosn, in the format of [[name, offset from begining of command], ...]
        #For eaxmple, if the cmd defines "start" as the first location in the command, and "end" as the fourth location, this would return the folowing:
        #[["start", 0], ["end", 3]]

    def emit(self):
        #This is where self.out would be written to
        pass
