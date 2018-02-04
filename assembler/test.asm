//Some Test code that doesn't do anything
/*Just for testing Assembler
NEW LINE COMMENT!!!*/
mov A B;

label code;
	in CX 0x12;
	mov CX A;
	put B 0x10;
	op OP_+;
	mov RES CND;
	jumpc code;

if (A*2) {
		out EX 12;
};

out (2+3*(BX + code)) 0x45;
