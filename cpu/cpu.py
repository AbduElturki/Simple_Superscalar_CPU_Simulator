from memory import reg

class CPU(object):
    def __init__(self,instruct):
        self.reset()
        self.init(instruct)
    def reset(self):
        self.pc = 0x00
        self.pc_next = 0x00
        self.reg = reg
        self.reg_next = reg
        self.running= False
        self.mem= ['00000000'] * 1024
    def init(self, instruct):
        self.instruction[:len(instruct)] = instruct
    def fetch(self):
        self.instruction_reg = self.instruction[self.pc]
        self.pc_next += 1
    def decode(self):
        self.op_reg = [self.instruct[self.pc][i:i+2] for i in [0,2,4,6]]
        if self.op[0] > 0x00:
            raise Exception('Negative Operand')
        elif self.op[0] >= 0x0A:
            #TODO something about linking Registers and ALU
            self.decoder = "ALU"

    def execute(self):
        if self.decoder is "ALU":
            ALU(self.op)

    def ALU(self):
        if self.op[0] is "01": #ADD
            r1 = "R"+op[1].replace("0","")
            r2 = "R"+op[2].replace("0","")
            r3 = "R"+op[3].replace("0","")
            self.reg_next[r1] = (self.reg[r2] + self.reg[r3]) % 0xFFFFFFFF
           
        elif self.op[0] is "02": #ADDI
            r1 = "R"+op[1].replace("0","")
            con = int(op[2] + op[3]) 
            self.reg_next[r1] = (self.reg[r1] + con) %  0xFFFFFFFF

        elif self.op[0] is "03": #SUB
            r1 = "R"+op[1].replace("0","")
            r2 = "R"+op[2].replace("0","")
            r3 = "R"+op[3].replace("0","")
            self.reg_next[r1] = (self.reg[r2] - self.reg[r3]) %  0xFFFFFFFF

        elif self.op[0] is "04": #MUL
            r1 = "R"+op[1].replace("0","")
            r2 = "R"+op[2].replace("0","")
            r3 = "R"+op[3].replace("0","")
            self.reg_next[r1] = (self.reg[r2] * self.reg[r3]) % 0xFFFFFFFF 
            
        elif self.op[0] is "05": #DIV
            r1 = "R"+op[1].replace("0","")
            r2 = "R"+op[2].replace("0","")
            r3 = "R"+op[3].replace("0","")
            self.reg_next[r1] = int(self.reg[r2] / self.reg[r3]) % 0xFFFFFFFF

        elif self.op[0] is "06": #XOR
            r1 = "R"+op[1].replace("0","")
            r2 = "R"+op[2].replace("0","")
            r3 = "R"+op[3].replace("0","")
            self.reg_next[r1] = (self.reg[r2] ^ self.reg[r3]) % 0xFFFFFFFF
            
        elif self.op[0] is "07": #SHL
            r1 = "R"+op[1].replace("0","")
            r2 = "R"+op[2].replace("0","")
            r3 = "R"+op[3].replace("0","")
            temp = (self.reg[r2] << self.reg[r3])
            self.reg_next[r3] = int(format(temp,'b')[:32], 2)

        elif self.op[0] is "08": #SHR
            r1 = "R"+op[1].replace("0","")
            r2 = "R"+op[2].replace("0","")
            r3 = "R"+op[3].replace("0","")
            temp = (self.reg[r2] >> self.reg[r3])
            self.reg_next[r3] = int(format(temp,'b')[:32], 2)

        elif self.op[0] is "09": #CMP
            r1 = "R"+op[1].replace("0","")
            r2 = "R"+op[2].replace("0","")
            r3 = "R"+op[3].replace("0","")
            if self.reg[r2] < self.reg[r3]:
                self.reg_next[r1] = int('1'*31+'0', 2) 
            elif self.reg[r2] == self/reg[r3]:
                self.reg_next[r1] = 0
            else:
                self.reg_next[r1] = 1

        elif self.op[0] is "02": #SUBI
            r1 = "R"+op[1].replace("0","")
            con = int(op[2] + op[3]) 
            self.reg_next[r1] = (self.reg[r1] - con) %  0xFFFFFFFF

        else:
            raise Exception("Unit control called ALU, however the opcode for ALU doesn't exist")
