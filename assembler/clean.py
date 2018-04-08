#Cleans up text assembley for macro handling and tokenization
class Clean:
    def __init__(self, asm):
        self.asm = asm;

    def removeComments(self):
        while self.asm.find("//") != -1:
            i = self.asm.find("//")
            nlI = self.asm.find("\n", i)
            self.asm = self.asm[:i] + self.asm[nlI:]
        while self.asm.find("/*") != -1:
            i = self.asm.find("/*")
            endI = self.asm.find("*/") + 2
            self.asm = self.asm[:i] + self.asm[endI:]
        return self.asm

    def hasBadWhitespace(self):
        white = ["\t", "  ", "\n", "{ ", "( ", " )", " }", "; ", " ;"]
        for p in white:
            if self.asm.find(p) != -1:
                return True
        return False

    def cleanWhitespace(self):
        replaces = [["\n", ""], ["  ", " "], ["\t", ""], ["{ ", "{"], ["( ", "("],
                    [" }", "}"], [" )", ")"], ["; ", ";"], [" ;", ";"]]
        while(self.hasBadWhitespace()):
            for r in replaces:
                self.asm = self.asm.replace(r[0], r[1])
        return self.asm

    def clean(self):
        self.removeComments()
        self.cleanWhitespace()
        return self.asm
