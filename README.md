# Comp16 Compilers
This is a collection of tools to generate code for my [Comp16 FPGA Microcomputer](https://github.com/darksteelcode/comp16). Software made with these tools is located in the [Comp16 Software](https://github.com/darksteelcode/comp16_software) respositry.

## Usage
Installation instructions are below.
### Assembler
To use, run:
```
c16asm -o outfile.bin asmfile.asm
```
### Transmit
To use, run:
```
sudo c16send -s serial_port binfile.bin
```
sudo is required as transmition uses a serial port.
## Installation
Installation is only for linux and mac. Because these tools are written in python, it could be run on windows. Because the installation compiles a python binary, it may take a few moments, but shouldn't take too long.
### Dependencies
python 2.7 and pyserial are required.
### Install
To install run the following:
```
cd ~
git clone https://github.com/darksteelcode/comp16_compilers.git
cd comp16_compilers
sudo make install
```
This will display usage instructions for the assembler, then prompt for a password for `sudo`. It has cloned `comp16_compilers` in your home directory, compiled the assembler to a pyc file, and linked a python file to run that pyc to `/usr/local/bin` as `c16asm`.
### Uninstall
To uninstall run the following:
```
cd ~/comp16_compilers
sudo make uninstall
cd ..
``` 

## Assembler
The assembler is located in `assembler`.

## Transmit
The transmiter is located in `transmit`. It contains tools to transmit programs over a uart to comp16. It is still in development, and can only transmit hex files, not comp16 binaries.

## Assembley Language Syntax
This section will not talk about general syntax for comp16 assembley, not specific commands.
### Basics
Each command contains a command, a space, then a number of arguments, seperated by spaces, and terminated by a semicolon. An argument to a command may include more code in brackets. For example:
```
ret;
lod A B;
loop A {mov A B;lod mem-1 FX;};
loop A {
    mov A B;
    lod mem-1 FX;
};
```
Whitespace outside of commands is ignored - Therefore, the third and fourth examples are the same. However, whitespace inside of commands does matter - the following is not valid: `mov A B ;`.
### Comments
Comp16 uses C-style comments - the following example should illustrate this
```
//A Comment
mov A B; //Another comment
/* A multi-line commont
Another Line
*/
lod A B;
```
### Values
Comp16 values are by default in decimal, but supports radixes of binary and hexidecimal, specified by `0x` and `0b` prefixes. For example:
```
123 //123
0x5f43 //24387
0b1010 //10
```
Because comp16 is 16-bit, high and low bytes can be spefified with `'h` and `'l` at the end of the number. `'l` does nothing to the number, and is included only for completness. `'h` shifts the number left 8 bits. This is useful for commands, such as `prb`, that take the top byte of a number. For example:
```
0xfa   //0x00fa
0xfa'l //0x00fa
0xfa'h //0xfa00 
```
# Comp16 Specification

IMPORTANT - This Specification is being worked on and is not complete.

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
### 3:jpc reg(4) addrs(8); Jump COnditional
jpc is the same as jmp, but only performs a jump if CND is a non zero value.
