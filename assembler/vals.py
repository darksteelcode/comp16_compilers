TYPE_REG = 0
TYPE_MEM = 1
TYPE_VAL = 2
TYPE_CODE = 3

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
        return "register"
    if n == 1:
        return "memory address"
    if n == 2:
        return "number"
    if n == 3:
        return "code"
    return "undefined"

def valToNum(val):
    if val[0] == "'" and val[-1] == "'":
        specials = ["\\", "\\'", "\\\"", "\\a", "\\b", "\\f", "\\n", "\\r", "\\t", "\\v"]
        vals = [47, 39, 34, 7, 8, 12, 10, 13, 9, 11]
        if not val[1:-1] in specials:
            return ord(val[1:-1])
        else:
            return vals[specials.index(val[1:-1])]
    radix = 10
    if val[0:2] == '0x':
        radix = 16
    if val[0:2] == '0b':
        radix = 2
    try:
        num = int(val, radix)
        return num
    except ValueError:
        return None
