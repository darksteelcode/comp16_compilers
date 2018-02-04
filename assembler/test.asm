//Some Test code that doesn't do anything
/*Just for testing Assembler
NEW LINE COMMENT!!!*/

label code;
. 'A';
. 'B';
. 'C';
. 'D';
label end;
out_addr start;
out_addr end;
label real_end;
. 0xffff;
out_addr real_end;
