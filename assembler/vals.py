'''
TYPES:
REGister: A, B, RES, PC, ...
MEMory address: a label name that is defined by a label cmd as a addr
TYPE_VALue: A number. Decimal by default, 0x prefix makes hex, 0b prefix makes binary. Ending with a 'h or 'l specifies high or low byte for cmds like prb. 'l does nothing, 'h shifts the number left a byte
'''

CHAR_SPECIALS = ["\\", "\\'", "\\\"", "\\a", "\\b", "\\f", "\\n", "\\r", "\\t", "\\v"]
CHAR_REPLACES = [47, 39, 34, 7, 8, 12, 10, 13, 9, 11]
SEPARATORS = [' ', ';', '\t', '\n']
TYPE_REG = 0
TYPE_MEM = 1
TYPE_VAL = 2
TYPE_CODE = 3
TYPE_ANY = 4

TYPE_NAMES = ["REG", "MEM", "VAL", "CODE", "ANY"]

REGS = ["A", "B", "RES", "PC", "MAR", "MDR", "CND", "BP", "SP", "CR", "AX", "BX", "CX", "DX", "EX", "FX"]

def getType(val):
    if val in REGS or val[0] == '(' and val[-1] == ')':
        return TYPE_REG
    if val[0] == '{' and val[-1] == '}':
        return TYPE_CODE
    if valToNum(val) != None:
        return TYPE_VAL
    return TYPE_MEM

def typeToName(n):
    if n == 0:
        return "REG"
    if n == 1:
        return "MEM"
    if n == 2:
        return "VAL"
    if n == 3:
        return "CODE"
    if n == 4:
        return "ANY"
    return "UNKNOWN"

def valToNum(val):
    if val[0] == "'" and val[-1] == "'":
        specials = CHAR_SPECIALS
        vals = CHAR_REPLACES
        if not val[1:-1] in specials:
            return ord(val[1:-1])
        else:
            return vals[specials.index(val[1:-1])]
    radix = 10
    shift = 0
    if val[0:2] == '0x':
        radix = 16
    if val[0:2] == '0b':
        radix = 2
    if val[-2:] == '\'h' or val[-2:] == '\'l':
        if val[-2:] == '\'h':
            shift = 8
        val = val[:-2]
    try:
        num = int(val, radix)
        num = num << shift
        return num
    except ValueError:
        return None
