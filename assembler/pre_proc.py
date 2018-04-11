from util import *
import vals
import macro
#Preprocessor
#NOTE - include looks in /usr/c16_include for asm files after current dir
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

#repeat 126
mov A B;
pra B 4;
\

'''
class Preprocessor:
    def __init__(self, asm):
    	self.asm = asm
    	#valid cmds in order to apply them - MACRO must come after defne and before the rest, else it's body will be preproc'd without arguments
    	self.valid = ["include", "define", "macro", "repeat", "string"]
    	#Already included files - don't include again
    	self.included = []
    	self.runs =  [self.include, self.define, self.macro, self.repeat, self.string]
    	self.instrs = [] #Instrs in string form
    	self.cmds = [] #Tokenized
    	#Valid seperators for command names
    	self.sprts = vals.SEPARATORS
    	#All macro variations defined
    	self.macros = []
    	#Processed macros with all variations
    	self.cleanMacros = []

    def applyInstr(self):
        for i in self.valid:
            firstInstr,index = self.findFirstAndRemove(i)
            while firstInstr:
                token = self.tokenizeInstr(firstInstr, index)
                func = self.runs[self.valid.index(i)]
                func(token)
                firstInstr,index = self.findFirstAndRemove(i)
        self.cleanMacros = self.consolidateMacros()
        return self.asm, self.cleanMacros

    def consolidateMacros(self):
        names = []
        macros = []
        for m in self.macros:
            if not m.name in names:
                macros.append(macro.Macro(m.name))
                macros[-1].addVariation(m)
                names.append(m.name)
            else:
                for i in macros:
                    if i.name == m.name:
                        i.addVariation(m)
        return macros

    def findFirstAndRemove(self, cmd):
        endIndex = 0
        index = 0
        index = self.asm.find("#", index)
        while index != -1:
            endIndex = self.asm.find('\\', index)
            if endIndex == -1:
                error("Preprocessor instruction not closed with an \\", self.asm[index:self.asm.find("\n", index+1)])
            instr = self.asm[index:endIndex+1]
            if instr.split(" ")[0] == "#"+cmd or instr[:instr.find("\n")] == "#"+cmd:
                self.asm = self.asm[:index] + self.asm[endIndex+1:]
                return instr, index
            index = self.asm.find("#", index+1)
        return False, False

    def tokenizeInstr(self, i, index):
        #Remove # and \
        i = i[1:-1]
        cmdEnd = i.find("\n")
        body = ""
        if cmdEnd != -1:
            body = i[cmdEnd:]
        else:
            cmdEnd = len(i)
        line1s = i[:cmdEnd].split(' ')
        return [line1s[0], line1s[1:], body, index]

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
            error("#define takes 2 arguments, not " + str(len(cmd[1])), "#" + cmd[0] + " " + ' '.join(cmd[1]))
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
        if len(cmd[1]) != 1:
            error("#include takes 1 arguments, not " + str(len(cmd[1])), "#" + cmd[0] + " " + ' '.join(cmd[1]))
        path = cmd[1][0]
        try:
            f = open(path)
        except IOError:
     	    try:
           	    f = open("/usr/c16_include/" + path)
            except IOError:
                error("No such file: " + path, "#" + cmd[0] + " " + ' '.join(cmd[1]))

        if not path in self.included:
            self.asm = self.asm[:cmd[3]] + f.read() + self.asm[cmd[3]:]
            self.included.append(path)
        f.close()

    def repeat(self, cmd):
        if len(cmd[1]) != 1:
            error("#repeat takes 1 arguments, not " + str(len(cmd[1])) + "-Text to repeat goes in body of #repeat", "#" + cmd[0] + " " + ' '.join(cmd[1]))
        try:
            num = vals.valToNum(cmd[1][0])
        except ValueError:
            error("#repeat takes a number as argument 0", "#" + cmd[0] + " " + ' '.join(cmd[1]))
        self.asm = self.asm[:cmd[3]] + cmd[2]*num + self.asm[cmd[3]:]

    def string(self, cmd):
        name = False
        if len(cmd[1]) != 0:
            if len(cmd[1]) == 1:
                name = cmd[1][0]
            else:
                error("#string takes 0 arguments, not " + str(len(cmd[1])) + "-String should be in body of #string", "#" + cmd[0] + " " + ' '.join(cmd[1]))
        result = ""
        if name:
            result += "label " + name + ";\n"
        cmd[2] = cmd[2][1:]
        for c in cmd[2]:
            if not ord(c) in vals.CHAR_REPLACES:
                result += ". '" + c + "';\n"
        result += ". 0;\n"
        self.asm = self.asm[:cmd[3]] + result + self.asm[cmd[3]:]

    def macro(self, cmd):
        if len(cmd[1]) < 1:
            error("#macro takes at least one argument - the macro name", "#" + cmd[0] + " " + ' '.join(cmd[1]))
        name = cmd[1][0]
        cmd[1] = cmd[1][1:]
        if len(cmd[1]) % 2 != 0:
            error("#macro needs a macro name, and each argument needs a type and name", "#" + cmd[0] + " " + ' '.join(cmd[1]))
        args = []
        for i in range(len(cmd[1])):
            if i%2==0:
                args.append([cmd[1][i], cmd[1][i+1]])
        #Convert string types to numbers
        for a in args:
            try:
                a[0] = vals.TYPE_NAMES.index(a[0])
            except ValueError:
                error("#macro arguments need to have a valid argument type - REG, MEM, CODE, ANY", "#" + cmd[0] + " " + ' '.join(cmd[1]))
        self.macros.append(macro.MacroVariation(name, args, cmd[2]))
