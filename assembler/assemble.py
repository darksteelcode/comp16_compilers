import sys
import args, clean
import token
import compiler
import pre_proc

def asmToCompilerRdyTokens(asm):
    asm, macros = pre_proc.Preprocessor(asm).applyInstr()
    asm = clean.Clean(asm).clean()
    tokens = token.Tokenizer(asm).getCmds()
    #tokens with macros applied
    finalTokens = []
    #Apply macros here
    for t in range(len(tokens)):
        appliedMacro = False
        for m in macros:
            if tokens[t].cmd == m.name:
                body = m.applyArgs(tokens[t].args)
                replaceTokens = asmToCompilerRdyTokens(body)
                finalTokens = finalTokens + replaceTokens
                appliedMacro = True
                break
        if not appliedMacro:
            finalTokens.append(tokens[t])
    return finalTokens

asmFile, outFile = args.getFiles()
asm = asmFile.read()
tokens = asmToCompilerRdyTokens(asm)
c = compiler.Compiler(tokens, outFile)
c.run()
print "Comp16 Assembler Finished Succesfully"
print str(outFile.tell()) + " bytes written"
if outFile.tell() == 0:
    print "Are you sure the file contains proper comp16 asm code?"
outFile.close()
