import base
import vals
from util import *

class pop(base.base):
    def initVars(self):
        self.types = [vals.TYPE_REG]
        self.lens = [4, 4]
        self.vals = [9]
        self.LENGTH = 1

    def emit(self):
        self.convToValues()
        #8 = SP
        out = intsToCmd([self.vals[0], 8, self.vals[1], 0], [4, 4, 4, 4])
        self.out.write(out)
