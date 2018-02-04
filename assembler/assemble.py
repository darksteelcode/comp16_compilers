import sys
import args, clean
import token
import compiler

asmFile, outFile = args.getFiles()
asm = asmFile.read()
asm = clean.Clean(asm).clean()
tokens = token.Tokenizer(asm).getCmds()
c = compiler.Compiler(tokens, outFile)
c.run()
