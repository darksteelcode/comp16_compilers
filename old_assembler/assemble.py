import sys

if len(sys.argv) < 2:
    print "- Comp16 Assembler -\nUsage:\npython assemble.py [options] [asm file]\nOptions:\n-o [output file]"
    exit()

path = sys.argv[len(sys.argv)-1]
asmFile = open(path)

def getFlags():
	index = 0
	flags = []
	for i in sys.argv:
		if i[0] != "-":
			index += 1
			continue
		flag = i[1:]
		#Dont interpret asm file as flag arg
		arg = False
		if index + 1 < len(sys.argv)-1:
			if sys.argv[index+1][0] != "-":
				arg = sys.argv[index+1]
		flags.append([flag, arg])
		index += 1
	return flags

print "- Comp16 Assembler -"

flgs = getFlags()
outPath = 'asm.bin'
for i in flgs:
	if i[0] == 'o' and i[1]:
		outPath = i[1]
print "Assembling " + path + " to " + outPath
print "--------------------\n"

def error(err, context):
    print "- Comp16 Assembler - \nError:\n" + str(err) + "\nAt:\n\n" + str(context) + "\n"
    exit()

#-----------  VARS -------------
'''
Types: val, mem, reg, any
val - value, determined at compile time, 16 bit
	decimal by default, 0x specifies hex, 0b binary, can start with h or l (high or low) (low is included for completness, doesn't do anything) to multiply by 256 to make data be high part of 16 bit value
		
mem - memory location, memory location determined during compolition
reg - one of 16 named registers
    A B RES PC MAR MDR CND BP SP CR AX BX CX DX EX FX

any - any type - used for macros that don't need to check type
'''

'''
Numbers

Default Decimal, 0x for hex, 0b for binary

'''

#----------- MACRO -------------

#Start MACROID at 0xf0000 to stop probable uses as label by other, non macro code
macro_vars = {'%MACROID':0xf0000}

def macro_getAndRemoveMacro(asm):
	macros = []
	macroStart = 0
	while True:
		macroStart = asm.find("#macro ")
		if macroStart == -1:
			break
		end = asm.find("#end", macroStart)
		if end == -1:
			error("Macro not closed correctly", asm[macroStart:asm.find("\n", macroStart)])
		macro = asm[macroStart:end]
		macro = macro.replace("#macro ", "")
		asm = asm[:macroStart] + asm[end+len('#end'):]
		macro = clean_removeWhitespace(macro)
		macros.append(macro)
	return macros, asm

def macro_procMacros(macros):
	proced = []
	for m in macros:
		head = m[:m.find(";")]
		body = m[m.find(";")+1:]
		headSplit = clean_splitArgs(head)
		name = headSplit[0]
		args = headSplit[1:]
		proced.append([name, args, body])
	return proced

def macro_applyProceds(proceds, call):
	for m in proceds:
		if m[0] != call[0]:
			continue
		cArgs = call[1:]
		callString = ' '.join(call) + ';'
		if len(m[1]) != len(cArgs):
			error("Macro " + m[0] + " requires " + str(len(m[1])) + " arguments, not " + str(len(cArgs)), callString)
		index = 0
		args = []
		names = []
		for a in m[1]:
			if a[0] != "{":
				args.append(cArgs[index])
				names.append(a)
				index += 1
				continue
			if cArgs[index][0] != "{":
				error("Argument #" + str(index)+1 + " on macro " + m[0] + " needs to be code", callString);
			args.append(cArgs[index][1:-1])
			names.append(a[1:-1])
			index += 1

		#Macro is good, just generate process now
		body = m[2]
		index = 0
		while index < len(args):
			body = body.replace(names[index], args[index])
			index += 1

		for v in macro_vars.keys():
			body = body.replace(v, str(macro_vars[v]))
		macro_vars['%MACROID']+=1
		return comp_AsmToOnlyAsm(body)
	return False

#----------- CLEAN -------------

clean_argGroupStart = ["(", "{"]
clean_argGroupEnd =   [")", "}"]

def clean_needWhitespaceRemoval(asm):
    white = ["\t", "  ", "\n", "{ ", "( ", " )", " }", "; ", " ;"]
    for p in white:
        if asm.find(p) != -1:
            return True
    return False

def clean_removeWhitespace(asm):
    #Replace Uneeded Whitespace
    replaces = [["\n", ""], ["  ", " "], ["\t", "  "], ["{ ", "{"], ["( ", "("],
                [" }", "}"], [" )", ")"], ["; ", ";"], [" ;", ";"]]
    while(clean_needWhitespaceRemoval(asm)):
        for r in replaces:
            asm = asm.replace(r[0], r[1])
    return asm

def clean_removeComments(asm):
    while asm.find("//") != -1:
        i = asm.find("//")
        nlI = asm.find("\n", i)
        asm = asm[:i] + asm[nlI:]

    while asm.find("/*") != -1:
        i = asm.find("/*")
        endI = asm.find("*/") + 2
        asm = asm[:i] + asm[endI:]

    return asm

def clean_splitArgs(asm):
    args = []
    depth = 0
    argStart = 0
    index = 0
    depth = 0
    for i in asm:
        if i in clean_argGroupStart:
            depth += 1
        elif i in clean_argGroupEnd:
            depth -= 1
        if depth < 0:
            error("To many closing " + i, asm[argStart:index+2])
        if i == " " and depth == 0:
            args.append(asm[argStart:index])
            argStart = index + 1
        index += 1
    args.append(asm[argStart:len(asm)])
    if depth != 0:
        error("All opening symbols not closed by end of command", asm)
    return args


def clean_splitCmdsAndArgs(asm):
    cmds = []
    depth = 0
    cmdStart = 0
    index = 0
    for i in asm:
        if i in clean_argGroupStart:
            depth += 1
        elif i in clean_argGroupEnd:
            depth -= 1
        if depth < 0:
            error("To many closing " + i, asm[cmdStart:index+2])
        if i == ";" and depth == 0:
            cmds.append(clean_splitArgs(asm[cmdStart:index]))
            cmdStart = index + 1
        index += 1
    if depth != 0:
        error("All opening symbols not closed by end of code", asm)
    return cmds

def comp_AsmToOnlyAsm(asm):
	asm = clean_removeComments(asm)
	asm = clean_removeWhitespace(asm)
	macros, asm = macro_getAndRemoveMacro(asm)
	macros = macro_procMacros(macros)
	calls = clean_splitCmdsAndArgs(asm)
	callIndex = 0
	for c in calls:
		apply = macro_applyProceds(macros, c)
		if apply:
			calls.pop(callIndex)
			index = callIndex
			for i in apply:
				calls.insert(index,i)
				index += 1
		callIndex += 1
	return calls



asm = asmFile.read()
print comp_AsmToOnlyAsm(asm)
