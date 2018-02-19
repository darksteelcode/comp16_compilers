import sys
import argparse
from util import *

parser = argparse.ArgumentParser(prog='PROG', add_help=False)
args = parser.parse_args()

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

def print_usage():
    print "- Comp16 Assembler -\nUsage:\npython assemble.py [options] <asm file>\nOptions:\n-o output file  (default: asm.bin)\n--------------------"

def getFiles():
    if len(sys.argv) < 2:
        print_usage()
        exit()

    try:
        path = sys.argv[len(sys.argv)-1]
        asmFile = open(path)
    except IOError:
        print_usage()
        nonASMError("No such file: " + path)
    print "- Comp16 Assembler -"

    flgs = getFlags()
    outPath = 'asm.bin'
    for i in flgs:
    	if i[0] == 'o' and i[1]:
    		outPath = i[1]
    	if i[0] == 'o' and not i[1]:
        	print_usage()
         	nonASMError("-o flag requires and output file")
    outFile = open(outPath, 'w')
    print "Assembling " + path + " to " + outPath
    print "--------------------"
    return asmFile, outFile;
