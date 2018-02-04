import sys
import args, clean

asmFile, outFile = args.getFiles()
asm = asmFile.read()
asm = clean.Clean(asm).clean();
print asm
