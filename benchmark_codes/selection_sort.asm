;R11 MEM location
;R12 Size
;R13 Size -1
;R9 outerloop
;R10 innerloop

LDI R11 0
LDI R12 8
SUBI R13 R12 1
LDI R9 0
LDI R10 1

;R6 address of numbers
;R14 CMP Result
outer_loop:
LDI R99 1 
MOV R6 R11
CMP R14 R9 R13
BEGZ R14 %outer_loop_end

;R14 CMP Result
;R2 first value Index
;R4 first value
;R3 Second value Index
;R5 Second value
inner_loop:
LDI R99 1 
CMP R14 R10  R12
BEGZ R14 %inner_loop_end

MOV R1 R9 
LD R4 R1

ADD R3 R10 R6
LD R5 R3 

CMP R14 R4 R5
BGZ R14 %swap

swap_return:
LDI R99 1 
ADDI R10 R10 1
JI %inner_loop

inner_loop_end:
LDI R99 1
ADDI R9 R9 1
ADDI R10 R9 1
JI %outer_loop

swap:
LDI R99 1 
ST R4 R3
ST R5 R1
JI %swap_return

outer_loop_end:
LDI R99 1 
