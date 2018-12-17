;R8 counter
;R2 start address 1
;R3 start address 2

LDI R8 8

;R7 condition
sortInts:
LDI R7 0
swappedLoop:
SUBI R8 R8 1
MOV R6 R8
LDI R2 -1
LDI R3 0
BZ R8 %exit
LDI R7 1
loopCount:
LDI R99 2
BZ R6 %swappedLoop
ADDI R2 R2 1
ADDI R3 R3 1
LD R4 R2
LD R5 R3
CMP R9 R4 R5
BGZ R9 %swap	
SUBI R6 R6 1
JI %loopCount

swap:
LDI R99 1
ST R5 R2
ST R4 R3
SUBI R6 R6 1
LDI R7 0
JI %loopCount

exit:
ADDI R11 1
