;R8 counter
;R2 start address 1
;R3 start address 2

LDI R8 8
LDI R2 -1
LDI R3 0

;R7 condition
sortInts:
LDI R7 0
swappedLoop:
MOV R6 R8
SUBI R6 R6 1
BGZ R7 %exit
LDI R7 1
loopCount:
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
