import base
import vals

class mov(base.base):
    def initVars(self):
        self.types = [vals.TYPE_REG, vals.TYPE_REG, vals.TYPE_VAL]
        self.lens = [4, 4, 4, 4]
        self.vals = [1]
        self.LENGTH = 1
