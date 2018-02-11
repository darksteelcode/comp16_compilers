//Some Test code that doesn't do anything
/*Just for testing Assembler
*/

nop 0xabc;
mov FX B;
label start;
jmp A start;
jpc MDR end;
. 12;
label end;
pra RES 0xaa;
prb CND 0xfa'h;
lod CND real_end;
str CND end;

label real_end;
psh A;
pop CND;
srt BX real_end;
ret;
ret 12;
out MDR 1;
in MAR 0xa;
