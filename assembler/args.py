import sys
import argparse
from util import *

parser = argparse.ArgumentParser(usage="\n--------------------\n- Comp16 Assembler -\nUsage:\npython assemble.py [options] <asm file>\nOptions:\n-o output file  (default: asm.bin)\n-h, --help display   help\n--------------------")
parser.add_argument("-o", nargs=1)
parser.add_argument("asm_file")
args = []

def genArgs():
    parser.parse_args()

def print_usage():
    print "usage:\n--------------------\n- Comp16 Assembler -\nUsage:\npython assemble.py [options] <asm file>\nOptions:\n-o output file  (default: asm.bin)\n-h, --help   display help\n--------------------"

def getFiles():
    path = args.asm_file
    outPath = 'asm.bin'
    if args.o:
        outPath = args.o[0]
    try:
        asmFile = open(path)
    except IOError:
        print_usage()
        nonASMError("No such file: " + path)
    print "- Comp16 Assembler -"
    outFile = open(outPath, 'w')
    print "Assembling " + path + " to " + outPath
    print "--------------------"
    return asmFile, outFile;
