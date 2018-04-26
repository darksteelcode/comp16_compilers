import sys, clean, token, compiler, pre_proc, macro, vals, macro_cmds


#Global list of macros is in vals

def asmToTokens(asm):
    asm, macros = pre_proc.Preprocessor(asm).applyInstr()
    vals.MACROS += macros
    asm = clean.Clean(asm).clean()
    tokens = token.Tokenizer(asm).getCmds()
    return tokens

def asmToCompilerRdyTokens(asm):
    tokens = asmToTokens(asm)
    tokens = macro.applyMacrosToTokens(tokens, vals.MACROS)
    tokens = macro_cmds.applyMacroCmds(tokens)
    return tokens

def run_c16asm():
    import args
    asmFile, outFile = args.getFiles()
    asm = asmFile.read()
    tokens = asmToCompilerRdyTokens(asm)
    for t in tokens:
        print t
    c = compiler.Compiler(tokens, outFile)
    c.run()
    print "Comp16 Assembler Finished Succesfully"
    print str(outFile.tell()) + " bytes written"
    if outFile.tell() == 0:
        print "Are you sure the file contains proper comp16 asm code?"
    outFile.close()
