LDI R1 0
LDI R2 1
LDI R9 19 

loop:
LDI R99 0
BZ R9 %exit
ADD R3 R2 R1
MOV R1 R2
MOV R2 R3
SUBI R9 R9 1
JI %loop

exit:
LDI R99 0
LDI R99 0