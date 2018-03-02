from util import *
#Preprocessor
#NOTE - include looks in /usr/c16-include for asm files
'''
Format
The begining of a preprocessor statment is marked by a #, and the end by a \
It is formated as follows

#cmd args
body
\

The body can be ommited if not used by the command, and the \ can be at the end of the last line instead

Examples:

#include data.asm\

#define A 3
\

'''
class Preprocessor:
    def __init__(self, asm):
    	self.asm = asm
    	self.valid = ["include", "define"]
    	self.runs =  [self.include, self.define]
    	self.instrs = [] #Instrs in string form
    	self.cmds = [] #Tokenized
    	#Valid seperators for command names
    	self.sprts = [' ', ';']

    #Takes code, gets instructions out, does not process them, and removes them from the asm
    def getAndRemoveInstr(self):
        endIndex = 0
        index = 0
        index = self.asm.find("#", index)
        while index != -1:
            endIndex = self.asm.find('\\', index)
            if endIndex == -1:
                error("Preprocessor instruction not closed with an \\", self.asm[index:self.asm.find("\n", index+1)])
            self.instrs.append(self.asm[index:endIndex+1])
            self.asm = self.asm[:index] + self.asm[endIndex+1:]
            index = self.asm.find("#", index+1)
    #Convert self.intrs to [[cmd, [args], body], ...]
    def tokenizeInstr(self):
        for i in self.instrs:
            #Remove # and \
            i = i[1:-1]
            cmdEnd = i.find("\n")
            body = ""
            if cmdEnd != -1:
                body = i[cmdEnd:]
            else:
                cmdEnd = len(i)
            line1s = i[:cmdEnd].split(' ')
	    self.cmds.append([line1s[0], line1s[1:], body])

    def runInstr(self):
        for i in self.cmds:
            if i[0] in self.valid:
	        index = self.valid.index(i[0])
                func = self.runs[index]
                func(i)
            else:
                error("Preprocessor command " + i[0] + " is not valid", "#" + i[0])

    #define cmd
    def define(self, cmd):
        if len(cmd[1]) != 2:
            error("#define takes 2 arguments, not " + str(len(cmd[1])), cmd[0] + " " + ' '.join(cmd[1]))
        old = cmd[1][0]
        new = cmd[1][1]
        index = self.asm.find(old)
        while index != -1:
            endIndex = len(self.asm) + 1
            for i in self.sprts:
                #Find next seperator
                ind = self.asm.find(i, index)
                if ind != -1 and ind < endIndex:
                    endIndex = ind
	    if self.asm[index:endIndex] == old and self.asm[index-1] in self.sprts:
           	self.asm = self.asm[:index] + new + self.asm[endIndex:]
            index = self.asm.find(old, index + 1)

    #include cmd
    def include(self, cmd):
        print "INCLUDE NOT YET IMPLEMENTED"


c = Preprocessor(open("CODE_TEST.asm").read())
c.getAndRemoveInstr()
c.tokenizeInstr()
c.runInstr()

print "----------"
print c.asm
