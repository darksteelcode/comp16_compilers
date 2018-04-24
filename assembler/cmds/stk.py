import base
import vals

class stk(base.base):
    def initVars(self):
        self.types = [vals.TYPE_REG, vals.TYPE_VAL]
        self.lens = [4, 4, 8]
        self.vals = [13]
        self.LENGTH = 1
