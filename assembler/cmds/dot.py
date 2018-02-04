import base
import vals
class dot(base.base):
    def initVars(self):
        self.lens = [16]
        self.types = [vals.TYPE_VAL]
        
    def emit(self):
        print "out_addr emiting"
