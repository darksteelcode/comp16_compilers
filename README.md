# Comp16 Compilers
This is a collection of tools to generate code for my [Comp16 FPGA Microcomputer](https://github.com/darksteelcode/comp16).

## Assembler
The assembler is located in `assembler`. Run `python assemble.py -o [output file (.bin)] [assembley file (.asm)]` to assemble a program.

## Comp16 Specification
Comp16 is a 16 bit microprocessor. All registers, memory and IO are operated on as 16 bit values.
### Registers
Comp16 has 16 registers, 8 of which have hardwire functions, 2 have fairly fixed roles in software, and 6 of which are general purpose.
The registers are, in the format `number in hex:shorthand:name - function`
```
                      _______________
0:A:A Reg ---------->|in0 Arithmetic |
1:B:B Reg ---------->|in1 Logic      |
2:RES:Result Reg <---|out Unit (ALU) |
                     |_______________|
3:PC:Program Counter Reg
4:MAR:Memory Address Reg
5:MDR:Memory Data Reg
6:CND:Conditional Reg
7:BP:Base Pointer
8:SP:Stack Pointer
9:CR:Construction Reg
a:AX:A General Purpose Reg
b:BX:B General Purpose Reg
c:CX:C General Purpose Reg
d:DX:D General Purpose Reg
e:EX:E General Purpose Reg
f:FX:F General Purpose Reg
```
