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
3:PC:Program Counter Reg - current location of program in memory (address of next instruction)
                              ______________________
4:MAR:Memory Address Reg --->|addr  MEMORY (16 bit  |
5:MDR:Memory Data Reg <----->|data  addr, 64k addr) |
                             |______________________|
6:CND:Conditional Reg - I this reg is a true value, a conditional jump will succeed, if it
is false, it will fail

7:BP:Base Pointer - NOT hard-coded, but used as a pointer to the stack pointer upon entry
to a function - a similar to a frame pointer on most architectures
8:SP:Stack Pointer - Hard-coded in srt and ret instr, and specified as first argument in
psh and pop. psh and pop should always use this as the stack pointer, and the assembler
doesn't allow changing this behavior

9:CR:Construction Reg - NOT hard-coded. Because a 16 bit value can't fit into one
instruction with an opcode, comp16 instructions operate on the high and low bytes of the
value. This register can be used to put the high and low bytes into, and then moved to a
register that changing one half an instruction earlier than the other half would lead to
unwanted behaviors (for example, the Program Counter - changing just one half would cause
an unwanted jump). Additional, this register can be used for instructions, such as jmp,
jpc, str, lod and srt that change the low byte of a register and then move it, in
combination with prb. For example, to jump to address 0xfa34:
  prb CR 0xfa'h;
  jmp CR 0x34;
The construction register's value should not be assumed to stay the same between subroutine
calls, jumps, and macros - use a general purpose register for that.

a:AX:A General Purpose Reg
b:BX:B General Purpose Reg
c:CX:C General Purpose Reg
d:DX:D General Purpose Reg
e:EX:E General Purpose Reg
f:FX:F General Purpose Reg
```
