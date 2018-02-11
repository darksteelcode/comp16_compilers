import base
import vals

class lod(base.base):
    def initVars(self):
        self.types = [vals.TYPE_REG, vals.TYPE_MEM]
        self.lens = [4, 4, 8]
        self.vals = [6]
        self.LENGTH = 1
