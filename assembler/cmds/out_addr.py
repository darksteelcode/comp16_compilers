import base
import vals
class out_addr(base.base):
    def initVars(self):
        self.lens = [16]
        self.types = [vals.TYPE_MEM]
    def emit(self):
        print "out_addr emiting"
