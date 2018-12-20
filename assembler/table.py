opcode = {
    "NOP" : 0x00,
    "HALT": 0x0f,
    #ALU
    "ADD" : 0x01,
    "ADDI": 0x02,
    "SUB" : 0x03,
    "MUL" : 0x04,
    "DIV" : 0x05,
    "XOR" : 0x06,

    "SHL" : 0x07,
    "SHR" : 0x08,

    "CMP" : 0x09,
    "SUBI": 0x0A,
    "VADD": 0x0B,
    "VSUB": 0x0C,
    "VMUL": 0x0D,
    "VDOT": 0x0E,
    #LOAD/STORE
    "LD"  : 0x10, #Load REG[OP1] into DMEM[R2]
    "LDI" : 0x11, #Load l1 into DMEM[R2]
    "ST"  : 0x12, #Store DMEM[R1] into REG[R2]
    "STO" : 0x13, #Store offset
    "LDO" : 0x14, #Load offset
    "MOV" : 0x15, #Move instruction
    "VLD" : 0x16,
    "VST" : 0x17,

    "J"   : 0x20, #Jump to address in register
    "JI"  : 0x21, #Jump to immediate address
    "JR"  : 0x22, #Jump relative
    "JAL" : 0x23, #Jump and store PC

    "BEGZ": 0x24, #Branch to Address in R2 if R1 >= 0
    "BLTZ": 0x25, #Branch to Address in R2 if R1 <  0
    "BZ"  : 0x26, #Branch to Address in R2 if R1 != 0
    "BGZ" : 0x27  #Branch to Address in R2 if R1 >  0
}

register_aliases = {
    "RV0" : "R8" ,
    "RV1" : "R9" ,
    "RF0" : "R10",
    "RF1" : "R11",
    "RS0" : "R12",
    "RS1" : "R13",

    "RA"  : "R14",
    "RSP" : "R15",
    "RHI" : "R16",
    "RZ"  : "R99",

    "VAX" : "R17",
    "VBX" : "R18",
    "VCX" : "R19",
    "VDX" : "R20",
    "VEX" : "R21",
    "VAS" : "R22",
    "VAL" : "R23",
    "VBS" : "R24",
    "VBL" : "R25",
    "VCS" : "R26",
    "VCL" : "R27",
    "VDS" : "R28",
    "VDL" : "R29",
    "VES" : "R30",
    "VEL" : "R31"
}
