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

def valToNum(val):
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
