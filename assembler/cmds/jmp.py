import base
import vals

class jmp(base.base):
    def initVars(self):
        self.types = [vals.TYPE_REG, vals.TYPE_MEM]
        self.lens = [4, 4, 8]
        self.vals = [2]
        self.LENGTH = 1
        self.opts = 0
