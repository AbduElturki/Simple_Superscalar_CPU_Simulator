from .op_unit import op_unit

class alu_logic(op_unit):
    def execute(self, cpu):
        decode = self.decode
        dest = decode[2]
        r2 = cpu.get_value(decode[3])
        r3 = cpu.get_value(decode[4])
        if decode[1] is 0x00: #ADD
            cpu.WBR[dest] = r2 + r3 % 0xFFFFFFFF 
            cpu.instruct_per_cycle[cpu.cycle] += 1
        elif decode[1] is 0x01: #SUB
            cpu.WBR[dest] = r2 - r3 % 0xFFFFFFFF 
            cpu.instruct_per_cycle[cpu.cycle] += 1
        elif decode[1] is 0x02: #MUL
            if self.cycle == 1:
                cpu.WBR[dest] = r2 * r3 % 0xFFFFFFFF 
                cpu.instruct_per_cycle[cpu.cycle] += 1
            else:
                self.cycle += 1
        elif decode[1] is 0x03: #DIV
            if self.cycle == 3:
                cpu.WBR[dest] = int(r2 / r3) % 0xFFFFFFFF 
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.cycle = 0
            else:
                self.cycle += 1
        elif decode[1] is 0x04: #XOR
            cpu.WBR[dest] = r2 ^ r3 % 0xFFFFFFFF 
            cpu.instruct_per_cycle[cpu.cycle] += 1
        elif decode[1] is 0x05: #SHL
            cpu.WBR[dest] = r2 << r3 % 0xFFFFFFFF 
            cpu.instruct_per_cycle[cpu.cycle] += 1
        elif decode[1] is 0x06: #SHR
            cpu.WBR[dest] = r2 >> r3 % 0xFFFFFFFF 
            cpu.instruct_per_cycle[cpu.cycle] += 1
        elif decode[1] is 0x07: #CMP
            cpu.WBR[dest] = int('1'*31+'0', 2) if r2 < r3 else 0 if r2 == r3 else 1
            cpu.instruct_per_cycle[cpu.cycle] += 1
