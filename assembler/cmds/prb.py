import base
import vals

class prb(base.base):
    def initVars(self):
        self.types = [vals.TYPE_REG, vals.TYPE_ANY]
        self.lens = [4, 4, 8]
        self.vals = [5]
        self.LENGTH = 1

    def handleSpecialVals(self):
        self.vals[2] = self.vals[2] >> 8
