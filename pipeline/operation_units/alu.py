from .op_unit import op_unit

class alu_logic(op_unit):
    def execute(self, cpu):
        decode = self.decode
        dest = decode[2]
        if decode[3] in cpu.retire_his:
            r2 = cpu.get_value(cpu.retire_his[decode[3]])
        else:
            r2 = cpu.get_value(decode[3])
        if decode[4] in cpu.retire_his:
            r3 = cpu.get_value(cpu.retire_his[decode[4]])
        else:
            r3 = cpu.get_value(decode[4])
        print(cpu.retire_his)
        if decode[1] == 0x00: #ADD 
            cpu.WBR[dest] = r2 + r3 % 0xFFFFFFFF 
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x01: #SUB
            cpu.WBR[dest] = r2 - r3 % 0xFFFFFFFF 
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x02: #MUL
            print(decode)
            if self.clock == 1:
                cpu.WBR[dest] = r2 * r3 % 0xFFFFFFFF 
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
        elif decode[1] == 0x03: #DIV
            if self.clock == 3:
                cpu.WBR[dest] = int(r2 / r3) % 0xFFFFFFFF 
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
        elif decode[1] == 0x04: #XOR
            cpu.WBR[dest] = r2 ^ r3 % 0xFFFFFFFF 
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x05: #SHL
            cpu.WBR[dest] = r2 << r3 % 0xFFFFFFFF 
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x06: #SHR
            cpu.WBR[dest] = r2 >> r3 % 0xFFFFFFFF 
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x07: #CMP
            cpu.WBR[dest] = int('1'*31+'0', 2) if r2 < r3 else 0 if r2 == r3 else 1
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        else:
            raise Exception(decode[0] +" " + decode[1] + ": doesn't exist in ALU")
