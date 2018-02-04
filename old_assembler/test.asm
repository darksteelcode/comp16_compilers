inf-mac {
	mov A B;
	put CR 123;
};

inf-loop {
	mov CR B;
};

#macro inf-loop {%code};
	//Infinite loop
  label %MACROID;
  %code
  jump %MACROID;
#end

#macro inf-mac {%cde};
	inf-loop {%cde};
#end

#macro if %reg {%code};
  mov %reg A;
  op OP_!;
  mov RES COND;
  jumpc %MACROID;
  %code
  label %MACROID;
#end
