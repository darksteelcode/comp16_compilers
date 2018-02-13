# Comp16 Compilers
This is a collection of tools to generate code for my [Comp16 FPGA Microcomputer](https://github.com/darksteelcode/comp16).

## Assembler
The assembler is located in `assembler`. Run `python assemble.py -o [output file (.bin)] [assembley file (.asm)]` to assemble a program.

## Comp16 Specification
Comp16 is a 16 bit microprocessor. All registers, memory and IO are operated on as 16 bit values. Because all the different parts of the architecture depend on each other, each section may not make complete sense the first time through.
### Registers
Comp16 has 16 registers, 8 of which have hardwire functions, 2 have fairly fixed roles in software, and 6 of which are general purpose. Each register is referenced by a 4-bit number.
The registers are, in the format `register number in hex:shorthand anme:name - function`
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
6:CND:Conditional Reg - If this reg is a true value, a conditional jump will succeed, if it
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
combination with prb. The construction register's value should not be assumed to stay the
same between subroutine calls, jumps, and macros - use a general purpose register for that.

a:AX:A General Purpose Reg
b:BX:B General Purpose Reg
c:CX:C General Purpose Reg
d:DX:D General Purpose Reg
e:EX:E General Purpose Reg
f:FX:F General Purpose Reg
```
### Instruction Set
Comp16 has 16 different instructions, 2 of which are un-implemented and do nothing. Each instruction fits into one 16-bit value in memory. Each instruction has a 4-bit opcode, followed by 12 bits of instruction arguments.

Because one instruction can't contain a 16 bit value and an opcode, some instructions operate on only one byte of a register. For example, the jumping `jmp` instruction takes two arguments, a register, and an 8-bit value. It puts that value into the lower half of the specified register, and moves it to the program counter. As memory addresses are 16-bit, an additional instruction is needed to jump to and address. This is a `prb`, which puts a value into the upper half or a register.

For example:
To jump to the address 0xf3a1, the following is used. (Note that the register uesed does not have to be the construction register, but it is good practice to use it for this purpose)
```
prb CR 0xf3'h; //Set the CR high byte equal to 0xf3. The 'h just specifies that this is the high byte being operated on.
jmp CR 0xa1; //Set the CR low byte equal to 0xa1, and move it to the PC, which will cause a jump once this instruction completes
```
The instructions are below, in the format `opcode in hex:shorthand-name argument(bit length) ...; name`
### 0:nop null(12); No Operation
nop does nothing, and just continues on to the next instruction. The argument does not matter.
Example:
```
nop; //Does nothing
nop 0xfff; //Does nothing again - argument does not matter
```
### 1:mov src-reg(4) dst-reg(4) alu-op(4); Move register
mov does two things - copies a register to a different register, and sets the ALU's mathematical operation. dst-reg is the reg to be copied into, src-reg is the reg with the value copied. alu-op is a the operation for the alu to perform (see the ALU section) (the alu op is optional in assembly language, and is set to zero if not specified).
Example:
```
mov RES A OP_<<; //Copy the value in the result register to the A register, and set the alu to do a left shift.
mov DX CND; //Copy the value in the F general purpose reg to the conditional register, and set the alu to do an addition (alu op 0).
```
### 2:jmp reg(4) addrs(8); Jump
jmp jumps to an adrs. It puts addrs into the lower byte of reg, then copies the value in reg to the program counter. Because `jmp` only affects the lower byte, it is used in conjunction with `prb`.
Example:
```
//jumps to the address 0xf3a1
prb CR 0xf3'h; //Set the CR high byte equal to 0xf3. The 'h just specifies that this is the high byte being operated on.
jmp CR 0xa1; //Set the CR low byte equal to 0xa1, and move it to the PC, which will cause a jump once this instruction completes.
```
