import base
import vals

class nop(base.base):
    def initVars(self):
        self.types = [vals.TYPE_VAL]
        self.lens = [4, 12]
        self.vals = [0]
        self.LENGTH = 1
        self.opts = 1
