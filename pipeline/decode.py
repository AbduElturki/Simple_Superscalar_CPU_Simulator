class decode_unit(object):
    def __init__(self, instruction, reg):
        self.instruct_reg = [self.instruction[self.pc][i:i+2] for i in [0,2,4,6]]
        self.mode = "ALU"
        self.decode = []
        self.decoder(reg)

    def decoder(self,reg):
        if self.instruct_reg[0] > 0x00:
            raise Exception('Negative Operand')
        
        #ALU
        #0x00 ADD | 0x04 XOR | 
        #0x01 SUB | 0x05 SHL | 
        #0x02 MUL | 0x06 SHR |
        #0x03 DIV | 0x07 CMP |

        elif self.instruct_reg[0] >= 0x0A:
            self.mode = "ALU"
            op = self.instruct_reg

            #Type-I ALU
            if self.instruct_reg[0] in [0x02, 0x0A]:
                r1 = "R"+op[1].replace("0","")
                if self.instruct_reg[0] is 0x02:
                    self.decode = [0x00, r1, reg[r1], int(op[2]+op[3])]
                elif self.instruct_reg[0] is 0x0A:
                    self.decode = [0x01, r1, reg[r1], int(op[2]+op[3])]
                else:
                    raise Exception("Tried to decode nonexistent Type I ALU opcode")

            #Type-R ALU
            else:
                r1 = "R"+op[1].replace("0","")
                r2 = "R"+op[2].replace("0","")
                r3 = "R"+op[3].replace("0","")
                if self.instruct_reg[0] is 0x01: #ADD
                    self.decode = [0x0, r1, reg[r2], reg[r3]]
                elif self.instruct_reg[0] is 0x03: #SUB
                    self.decode = [0x1, r1, reg[r2], reg[r3]]
                elif self.instruct_reg[0] is 0x04: #MUL
                    self.decode = [0x2, r1, reg[r2], reg[r3]]
                elif self.instruct_reg[0] is 0x05: #DIV
                    self.decode = [0x3, r1, reg[r2], reg[r3]]
                elif self.instruct_reg[0] is 0x06: #DIV
                    self.decode = [0x4, r1, reg[r2], reg[r3]]
                elif self.instruct_reg[0] is 0x07: #DIV
                    self.decode = [0x5, r1, reg[r2], reg[r3]]
                elif self.instruct_reg[0] is 0x08: #DIV
                    self.decode = [0x6, r1, reg[r2], reg[r3]]
                elif self.instruct_reg[0] is 0x09: #DIV
                    self.decode = [0x7, r1, reg[r2], reg[r3]]
                else:
                    raise Exception("Tried to decode nonexistent Type I ALU opcode")
