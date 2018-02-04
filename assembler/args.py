import sys
from util import *

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

def getFiles():
    if len(sys.argv) < 2:
        print "- Comp16 Assembler -\nUsage:\npython assemble.py [options] [asm file]\nOptions:\n-o [output file]"
        exit()

    try:
        path = sys.argv[len(sys.argv)-1]
        asmFile = open(path)
    except IOError:
        nonASMError("No such file: " + path)
    print "- Comp16 Assembler -"

    flgs = getFlags()
    outPath = 'asm.bin'
    for i in flgs:
    	if i[0] == 'o' and i[1]:
    		outPath = i[1]
    outFile = open(outPath, 'w')
    print "Assembling " + path + " to " + outPath
    print "--------------------"
    return asmFile, outFile;
