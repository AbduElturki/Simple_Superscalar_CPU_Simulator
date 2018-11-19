class decode_unit(object):
    def __init__(self):
        self.busy = False
        self.instruct_reg = None 
        self.mode = "ALU"
        self.decode = []
        #self.decoder(reg)

    def decoder(self, cpu):
        self.instruct_reg = [cpu.instruct_reg[i:i+2] for i in [0,2,4,6]]
        self.instruct_reg[0] = int(self.instruct_reg[0],16)
        op = self.instruct_reg

        r1 = "R"+str(int(op[1],16))
        r2 = "R"+str(int(op[2],16))
        r3 = "R"+str(int(op[3],16))

        if self.instruct_reg[0] < 0x00:
            raise Exception('Negative Operand')
        

        #ALU
        #0x00 ADD | 0x04 XOR | 
        #0x01 SUB | 0x05 SHL | 
        #0x02 MUL | 0x06 SHR |
        #0x03 DIV | 0x07 CMP |

        elif self.instruct_reg[0] <= 0x0A or self.instruct_reg[0] == 0x15:
            self.mode = "ALU"

            #Type-I ALU
            if self.instruct_reg[0] in [0x02, 0x0A]:
                r1 = "R"+str(int(op[1],16))
                if self.instruct_reg[0] is 0x02:
                    self.decode = [0x00, r1, cpu.reg[r1], int(op[2]+op[3], 16)]
                elif self.instruct_reg[0] is 0x0A:
                    self.decode = [0x01, r1, cpu.reg[r1], int(op[2]+op[3], 16)]
                else:
                    raise Exception("Tried to decode nonexistent Type I ALU opcode")

            #Type-R ALU
            else:


                if self.instruct_reg[0] is 0x01: #ADD
                    self.decode = [0x0, r1, r2, r3]
                elif self.instruct_reg[0] is 0x03: #SUB
                    self.decode = [0x1, r1, r2, r3]
                elif self.instruct_reg[0] is 0x04: #MUL
                    self.decode = [0x2, r1, r2, r3]
                elif self.instruct_reg[0] is 0x05: #DIV
                    self.decode = [0x3, r1, r2, r3]
                elif self.instruct_reg[0] is 0x06: #DIV
                    self.decode = [0x4, r1, r2, r3]
                elif self.instruct_reg[0] is 0x07: #DIV
                    self.decode = [0x5, r1, r2, r3]
                elif self.instruct_reg[0] is 0x08: #DIV
                    self.decode = [0x6, r1, r2, r3]
                elif self.instruct_reg[0] is 0x09: #DIV
                    self.decode = [0x7, r1, r2, r3]
                elif self.instruct_reg[0] is 0x15: #MOV
                    self.decode = [0x0, r1, r2, "R8"]
                else:
                    raise Exception("Tried to decode nonexistent Type R ALU opcode")

        elif self.instruct_reg[0] <= 0x14:
            self.mode = "DT"
            r1 = "R"+str(int(op[1],16))
            if self.instruct_reg[0] is 0x10: #LD
                self.decode = [0x0, r1, int(op[2]+op[3], 16)] 
            elif self.instruct_reg[0] is 0x11: #LDI
                self.decode = [0x1, r1, int(op[2]+op[3], 16)] 
            elif self.instruct_reg[0] is 0x12: #ST
                self.decode = [0x2, r1, int(op[2]+op[3], 16)]
            elif self.instruct_reg[0] is 0x13: #STO
                self.decode = [0x3, r1, int(op[2], 16), int(op[3], 16)]
            elif self.instruct_reg[0] is 0x14: #LDO
                self.decode = [0x4, r1, int(op[2], 16), int(op[3], 16)]
            else:
                raise Exception("Tried to decode nonexistent Data Transfer instruction") 

        elif self.instruct_reg[0] <= 0x27:
            self.mode = "CF"
            #TODO Add offsets
            if self.instruct_reg[0] is 0x20: #J
                self.decode = [0x0, op[1], r2]
            elif self.instruct_reg[0] is 0x21: #JI
                self.decode = [0x1, op[1], op[2]]
            elif self.instruct_reg[0] is 0x22: #JR
                self.decode = [0x2, op[1]]
            elif self.instruct_reg[0] is 0x23: #JAL
                self.decode = [0x3, op[1], r2]

            elif self.instruct_reg[0] is 0x24: #BEGZ
                self.decode = [0x4, "EGZ", r1, r2]
            elif self.instruct_reg[0] is 0x25: #BLTZ
                self.decode = [0x4, "LZ", r1, r2]
            elif self.instruct_reg[0] is 0x26: #BZ
                self.decode = [0x4, "Z", r1, r2]
            elif self.instruct_reg[0] is 0x27: #BGZ
                self.decode = [0x4, "GZ", r1, r2]
            else:
                raise Exception("Tried to decode nonexistent Controlflow instruction") 
