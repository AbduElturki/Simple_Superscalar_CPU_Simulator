class decode_unit(object):
    def __init__(self):
        self.busy = False
        self.instruct_reg = None 

    def check_if_free(self, cpu, instruct):
        opcode = int(instruct[:2], 16)
        if opcode in range(0x01, 0x0F) or opcode is 0x15:
            return cpu.is_unit_free("ALU")
        elif opcode in range(0x10, 0x18) and opcode is not 0x15:
            return cpu.is_unit_free("DT")
        elif opcode in range(0x20, 0x28):
            return cpu.is_unit_free("CF")
        else:
            raise Exception("Unit doesn't exist " + str(opcode))
            

    def decoder(self, cpu):
        cpu.retire_his = {}
        if not cpu.is_stalling():
            while len(cpu.instruct_buffer):
                if self.check_if_free(cpu, cpu.instruct_buffer[0]):
                    instruct = cpu.instruct_buffer.popleft() 
                    self.decode(cpu, instruct, False)
                    cpu.his_rat = cpu.rat.copy()
                    if cpu.is_stalling():
                        break
                else:
                    cpu.stall()
                    break
            if cpu.is_speculative():
                while len(cpu.instruct_fork[cpu.speculate_mode()]):
                    if self.check_if_free(cpu,
                                          cpu.instruct_fork[cpu.speculate_mode()][0]):
                        instruct = cpu.instruct_fork[cpu.speculate_mode()].popleft()
                        self.decode(cpu, instruct, True)
                    if cpu.is_stalling():
                        break
                    else:
                        cpu.stall()
                        break

    def decode(self, cpu, instruct, spec):
        self.instruct_reg = [instruct[i:i+2] for i in [0,2,4,6]]
        self.instruct_reg[0] = int(self.instruct_reg[0],16)
        op = self.instruct_reg

        r1 = "R"+str(int(op[1],16))
        r2 = "R"+str(int(op[2],16))
        r3 = "R"+str(int(op[3],16))

        if self.instruct_reg[0] < 0x00:
            raise Exception('Negative Operand')
        
        elif self.instruct_reg[0] <= 0x0E or self.instruct_reg[0] == 0x15:
            #Type-I ALU
            if self.instruct_reg[0] in [0x02, 0x0A]:
                r2 = cpu.get_dest(r2)
                cpu.new_dest(r1, spec)
                r1 = cpu.get_dest(r1)
                if self.instruct_reg[0] is 0x02:
                    decode = ["ALU", 0x00, r1, r2, int(op[3], 16)]
                elif self.instruct_reg[0] is 0x0A:
                    decode = ["ALU", 0x01, r1, r2, int(op[3], 16)]
                else:
                    raise Exception("Tried to decode nonexistent Type I ALU opcode")

            #Type-R ALU
            else:
                r2 = cpu.get_dest(r2)
                r3 = cpu.get_dest(r3)
                cpu.new_dest(r1, spec)
                r1 = cpu.get_dest(r1)

                if self.instruct_reg[0] is 0x01: #ADD
                    decode = ["ALU", 0x0, r1, r2, r3]
                elif self.instruct_reg[0] is 0x03: #SUB
                    decode = ["ALU", 0x1, r1, r2, r3]
                elif self.instruct_reg[0] is 0x04: #MUL
                    decode = ["ALU", 0x2, r1, r2, r3]
                elif self.instruct_reg[0] is 0x05: #DIV
                    decode = ["ALU", 0x3, r1, r2, r3]
                elif self.instruct_reg[0] is 0x06: #DIV
                    decode = ["ALU", 0x4, r1, r2, r3]
                elif self.instruct_reg[0] is 0x07: #DIV
                    decode = ["ALU", 0x5, r1, r2, r3]
                elif self.instruct_reg[0] is 0x08: #DIV
                    decode = ["ALU", 0x6, r1, r2, r3]
                elif self.instruct_reg[0] is 0x09: #DIV
                    decode = ["ALU", 0x7, r1, r2, r3]
                elif self.instruct_reg[0] is 0x15: #MOV
                    decode = ["ALU", 0x0, r1, r3, 0]
                elif self.instruct_reg[0] is 0x0B:
                    decode = ["ALU", 0x8, r1, r2, r3]
                elif self.instruct_reg[0] is 0x0C:
                    decode = ["ALU", 0x9, r1, r2, r3]
                elif self.instruct_reg[0] is 0x0D:
                    decode = ["ALU", 0xA, r1, r2, r3]
                elif self.instruct_reg[0] is 0x0E:
                    decode = ["ALU", 0xB, r1, r2, r3]
                else:
                    raise Exception("Tried to decode nonexistent Type R ALU opcode")

        elif self.instruct_reg[0] <= 0x17 and self.instruct_reg[0] is not 0x15:
            if self.instruct_reg[0] is 0x10: #LD
                r3 = cpu.get_dest(r3)
                cpu.new_dest(r1, spec)
                r1 = cpu.get_dest(r1)
                decode = ["DT", 0x0, r1, r3] 
            elif self.instruct_reg[0] is 0x11: #LDI
                cpu.new_dest(r1, spec)
                r1 = cpu.get_dest(r1)
                decode = ["DT", 0x1, r1, int(op[2] + op[3], 16)] 
            elif self.instruct_reg[0] is 0x12: #ST
                r1 = cpu.get_dest(r1)
                r2 = cpu.get_dest(r2)
                decode = ["DT", 0x2, r1, r3]
            elif self.instruct_reg[0] is 0x13: #STO
                r1 = cpu.get_dest(r1)
                r3 = cpu.get_dest(r3)
                decode = ["DT", 0x3, r1, int(op[2], 16), r3]
            elif self.instruct_reg[0] is 0x14: #LDO
                r3 = cpu.get_dest(r3)
                cpu.new_dest(r1, spec)
                r1 = cpu.get_dest(r1)
                decode = ["DT", 0x4, r1, int(op[2], 16), r3]
            elif self.instruct_reg[0] is 0x16: #LDO
                r3 = cpu.get_dest(r3)
                cpu.new_dest(r1, spec)
                r1 = cpu.get_dest(r1)
                decode = ["DT", 0x5, r1, r3]
            elif self.instruct_reg[0] is 0x17: #LDO
                r1 = cpu.get_dest(r1)
                r3 = cpu.get_dest(r3)
                decode = ["DT", 0x6, r1, r3]
            else:
                raise Exception("Tried to decode nonexistent Data Transfer instruction") 

        elif self.instruct_reg[0] <= 0x27:
            if self.instruct_reg[0] is 0x20: #J
                r1 = cpu.get_dest(r1)
                decode = ["CF", 0x0, r3]
            elif self.instruct_reg[0] is 0x21: #JI
                decode = ["CF", 0x1, int(op[1] + op[2] + op[3], 16)]
            elif self.instruct_reg[0] is 0x22: #JR
                decode = ["CF", 0x2, int(int[1] + op[2] + op[3], 16)]
            elif self.instruct_reg[0] is 0x23: #JAL
                decode = ["CF", 0x3, int(op[1] + op[2] + op[3], 16)]

            elif self.instruct_reg[0] is 0x24: #BEGZ
                r1 = cpu.get_dest(r1)
                decode = ["CF", 0x4, r1, int(op[2]+op[3], 16)]
            elif self.instruct_reg[0] is 0x25: #BLTZ
                r1 = cpu.get_dest(r1)
                decode = ["CF", 0x5, r1, int(op[2]+op[3], 16)]
            elif self.instruct_reg[0] is 0x26: #BZ
                r1 = cpu.get_dest(r1)
                decode = ["CF", 0x6, r1, int(op[2]+op[3], 16)]
            elif self.instruct_reg[0] is 0x27: #BGZ
                r1 = cpu.get_dest(r1)
                decode = ["CF", 0x7, r1, int(op[2]+op[3], 16)]
            else:
                raise Exception("Tried to decode nonexistent Controlflow instruction") 
        else:
            raise Exception("Opcode doesn't exist")
        cpu.load_to_rs(decode, spec)
