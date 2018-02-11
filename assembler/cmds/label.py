import base
import vals

class label(base.base):
    def initVars(self):
        self.lens = [16]
        self.types = [vals.TYPE_MEM]
        self.LENGTH = 0

    def getMemDefines(self):
        return [[self.cmd.args[0], 0]]

    def emit(self):
        #Label doesn't write anything
        pass
