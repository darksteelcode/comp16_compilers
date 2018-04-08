def error(err, context):
    print "- Comp16 Assembler - \nError:\n" + str(err) + "\nAt:\n\n" + str(context) + "\n"
    exit(1)

def nonASMError(err):
    print "- Comp16 Assembler - \nError:\n" + str(err)
    exit(1)

def intsToCmd(vals, lens):
    #vals is array of ints to make command, lens is length in bits of each
    result = 0
    lenI = 0
    for i in vals:
        cur = i & (2**(lens[lenI])-1)
        result += cur
        if lenI < len(lens)-1:
            result <<= lens[lenI + 1]
        lenI += 1
    if result >= 65536:
        error("Internal Error: to large values passed to intsToCmd in util.py", "None")
    return chr(result >> 8) + chr(result & 255)
