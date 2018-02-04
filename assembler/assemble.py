import sys
import args, clean
import token

asmFile, outFile = args.getFiles()
asm = asmFile.read()
asm = clean.Clean(asm).clean();
tokens = token.Tokenizer(asm).getCmds()
print tokens
