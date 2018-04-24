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

    def getResult(self):
        cmd = self.args[0]
        self.args = self.args[1:]
        self.types = self.types[1:]
        asm = ""
        for a, t in zip(self.args, self.types):
            if t == vals.TYPE_REG:
                asm += "psh " + a + ";"
            elif t == vals.TYPE_VAL:
                asm += "prb CR " + a + ";pra CR " + a + ";psh CR;"
            elif t == vals.TYPE_MEM:
                asm += "prb MAR " + a + ";lod CR " + a + ";psh CR;"
            else:
                error("call only takes REG, VAL, or MEM as arguments to function", self.asm)
        asm += "srt " + cmd + ";"
        return assemble.asmToTokens(asm)

'''
Call stack and functon entry and exit
(upward growing stack)

Arg 1    <- SP location on entry to function called in function, and during execution
-----
Local 3
Local 2
Local 1  <- SP location on entry to function and exit
Return Addrs
Arg 3
Arg 2
Arg 1    <- SP location after exit from function
--------
'''

#Defines func command, and takes care of local command
class func(MacroCmdBase):
    def setName(self):
        self.name = "func"

    def checkArgs(self):
        if len(self.args) < 2:
            error("func takes at least two arguments - a function name and code", self.asm)
        elif self.types[0] != vals.TYPE_MEM:
            error("the first argument to func has to be a function name (memory location)", self.asm)
        elif self.types[-1] != vals.TYPE_CODE:
            error("the last argument to func has to be code", self.ams)
        for t in self.types[1:-1]:
            if t != vals.TYPE_MEM:
                error("func's arguments can't be code, values, or registers", self.asm)
        return True

    def getResult(self):
        name = self.args[0]
        code = self.args[-1]
        #argument names - these are replaced in the body
        args = self.args[1:-1]
        #local names - thse are replaced in the body
        local = []
        #Remove { and } from code, and tokenize to simplest form
        code = assemble.asmToCompilerRdyTokens(code[1:-1])
        #Look through code for local definitions, add to local
        for c in code:
            if c.cmd == "local":
                if len(c.args) != 1:
                    error("local takes only one argument", c.toAsm())
                elif c.types[0] != vals.TYPE_MEM:
                    error("local's argment has to be a local var name (memory location)", c.toAsm())
                local.append(c.args[0])
        #Remove all local commands from code
        numArgs = len(args)
        numLocals = len(local)
        




a = func(["func_name", "arg1", "arg2", "{local loc1;prb A arg1;mov loc1 A;local loc2;mov loc2 AX;}"])
a.checkArgs()
a.getResult()
