#Macro commands are effectivley macros programmed in python
import vals
import assemble
from util import *

class MacroCmdBase:
    #Args are a list of args the macro is called with
    def __init__(self, args):
        self.args = args
        self.types = []
        self.genTypes()
        self.asm = ""
        self.setName()
        self.asm += self.name
        for i in self.args:
            self.asm += " " + i
        self.asm += ";"

    def genTypes(self):
        for a in self.args:
            self.types.append(vals.getType(a))

    def setName(self):
        self.name = "base"

    def checkArgs(self):
        #If an error occurs, print a message here
        return True

    #Return tokens to add in to the code
    def getResult():
        return []

class call(MacroCmdBase):
    def setName(self):
        self.name = "call"

    def checkArgs(self):
        if len(self.args) < 1:
            error("call takes at least one argument", self.asm)
        if self.types[0] != vals.TYPE_MEM:
            error("the first argument to call has to be a memory location", self.asm)
        return True

    def getResult(self):
        cmd = self.args[0]
        self.args = self.args[1:]
        self.types = self.types[1:]
        asm = ""
        for a, t in zip(self.args, self.types):
            if t == vals.TYPE_REG:
                asm += "psh " + a + ";"
            elif t == vals.TYPE_VAL:
                asm += "prb CR " + a + ";pra CR " + a + ";psh CR;"
            elif t == vals.TYPE_MEM:
                asm += "prb MAR " + a + ";lod CR " + a + ";psh CR;"
            else:
                error("call only takes REG, VAL, or MEM as arguments to function", self.asm)
        asm += "srt " + cmd + ";"
        return assemble.asmToTokens(asm)

'''
Call stack and functon entry and exit
(upward growing stack)

Arg 1    <- SP location on entry to function called in function, and during execution
-----
Local 2
Local 1  <- SP location on entry to function and exit
Return Addrs
Arg 3
Arg 2
Arg 1    <- SP location after exit from function
--------

Function Entry and Exit (n is number of arguments, l is number of locals on stack)
Entry
mov SP A OP_-;
prb B l;
pra B l;
mov RES SP;

Exit
mov SP A OP_+;
prb B l;
pra B l;
mov RES SP;
ret n;


'''

#Defines func command, and takes care of local command
class func(MacroCmdBase):
    def setName(self):
        self.name = "func"

    def checkArgs(self):
        if len(self.args) < 2:
            error("func takes at least two arguments - a function name and code", self.asm)
        elif self.types[0] != vals.TYPE_MEM:
            error("the first argument to func has to be a function name (memory location)", self.asm)
        elif self.types[-1] != vals.TYPE_CODE:
            error("the last argument to func has to be code", self.ams)
        for t in self.args[1:-1]:
            if t[0] != "$":
                error("func arguments must be prefixed with an $ (they go on the stack", self.asm)
        return True

    def getResult(self):
        name = self.args[0]
        code = self.args[-1]
        #argument names - these are replaced in the body
        args = self.args[1:-1]
        #local names - thse are replaced in the body
        local = []
        #Remove { and } from code, and tokenize to simplest form
        code = assemble.asmToCompilerRdyTokens(code[1:-1])
        #Look through code for local definitions, add to local
        for c in code:
            if c.cmd == "local":
                if len(c.args) != 1:
                    error("local takes only one argument", c.toAsm())
                elif c.args[0][0] != "$":
                    error("all variables on the stack need to start with an $", c.toAsm())
                local.append(c.args[0])
        #Remove all local commands from code
        code = [t for t in code if (t.cmd != "local")]
        #Count number of element needed on stack in preparation for function entry and exit code
        numArgs = len(args)
        numLocals = len(local)
        #Generate Function entry and exit code
        entryCode = "mov SP A 1;prb B " + str(numLocals) + ";pra B " + str(numLocals) + ";mov RES SP;"
        exitCode = "mov SP A 0;prb B " + str(numLocals) + ";pra B " + str(numLocals) + ";mov RES SP;ret " + str(numArgs) + ";"
        entryCode = assemble.asmToTokens(entryCode)
        exitCode = assemble.asmToTokens(exitCode)
        #final set of tokens to return
        tokens = []
        tokens += entryCode
        #generate array with variables on stack with the format: [[name, num_to_sub_from_SP], ...]
        stack_vars = []
        index_add = 1
        for l in reversed(local):
            stack_vars.append([l, index_add])
            index_add += 1
        stack_vars.append(["FUNC_RETURN_ADDRS", index_add])
        index_add += 1
        for a in reversed(args):
            stack_vars.append([a, index_add])
            index_add += 1
        print stack_vars
        #Replace each stack argument in the code with code to load its address in MAR (skl sks), and appropriatley replace the argument
        #Replace cases to deal with (* marks an automatic case - if command reads, do skl BP before, if write, do sks BP after):
        ''''
        mov reg $var - sks reg $var;
        mov $var reg - skl reg $var;
        mov $var1 $var2 - skl BP $var1;sks BP $var2;

        jmp $var loc - skl BP $var;jmp BP loc;*
        jpc $var loc - skl BP $var;jpc BP loc;*

        pra $var val - skl BP $var;pra BP val;sks BP $var;
        prb $var val - skl BP $var;prb BP val;sks BP $var;

        lod $var loc - lod BP loc;sks BP $var;*
        str $var loc - skl BP $var;str BP loc;*

        psh $var - skl BP $var;psh BP;*
        pop $var - pop BP;sks BP $var;*

        srt $var loc - skl BP $var;srt BP loc;*

        out $var port - skl BP $var;out BP port;*
        in $var port - in BP port;sks BP $var;*
        ''''




a = func(["func_name", "$arg1", "$arg2", "$arg3", "{local $loc1;prb A $arg1;pra B AX;mov $loc1 A;local $loc2;mov $loc2 AX;}"])
a.checkArgs()
a.getResult()
