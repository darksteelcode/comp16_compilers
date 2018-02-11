import base
import vals

class srt(base.base):
    def initVars(self):
        self.types = [vals.TYPE_REG, vals.TYPE_MEM]
        self.lens = [4, 4, 8]
        self.vals = [10]
        self.LENGTH = 1
