import base
import vals

class Str(base.base):
    def initVars(self):
        self.types = [vals.TYPE_REG, vals.TYPE_MEM]
        self.lens = [4, 4, 8]
        self.vals = [7]
        self.LENGTH = 1
