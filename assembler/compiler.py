'''
This is the last pass before the binary file is outputed.
Compiler does the following:
    1. create a command class for each cmd
    2. resolve mem variables to real addresses by asking each command if it defines a mem address, and based on each commands length
    3. lets each cmd emit its output to the binary file
       (for complex commands like subroutines, this coud contain recursive code evaluation)

ARGS:
cmds is list of Cmd from token.py
out is output file
'''

from cmds import base, dot, label, out_addr
from util import *
import vals

#CMD_NAMES = ["nop", "mov", "jmp", "jpc", "pra", "prb", "lod", "str", "psh", "pop", "srt", "ret", "out", "in"]
'''
. and label are real, out_addr is just for testing
cmds:
. data  - set instr equal to data
label data - set mem addrs data equal to current pos
out_addr data - set instr equal to real addrs of label data
'''
CMD_NAMES = [".", "label", "out_addr"]
CMD_CLASSES = [dot.dot, label.label, out_addr.out_addr]

class Compiler:
    def __init__(self, cmds, out):
        self.tokens = cmds
        self.cmds = []
        self.out = out
        self.mems = []

    def initCmds(self):
        for t in self.tokens:
            try:
                classI = CMD_NAMES.index(t.cmd)
            except ValueError:
                error("Command " + t.cmd + " is not defined", t.toAsm())
            self.cmds.append(CMD_CLASSES[classI](t, self.out));
            self.cmds[-1].assignCompiler(self)

    def resolveMem(self):
        memAddr = 0
        for c in self.cmds:
            memDefs = c.getMemDefines()
            for m in memDefs:
                self.mems.append([m[0], memAddr + m[1]])
            memAddr += c.LENGTH
        print self.mems

    def getValue(self, val):
        val_type = vals.getType(val)
        if val_type == vals.TYPE_VAL:
            return vals.valToNum(val)
        if val_type == vals.TYPE_REG:
            return vals.REGS.index(val)
        if val_type == vals.TYPE_MEM:
            for m in self.mems:
                if m[0] == val:
                    return m[1]
            error("Memory address " + val + " is not defined", val)
        error("Name " + val + " is not defined", val)

    def run(self):
        self.initCmds()
        self.resolveMem()
