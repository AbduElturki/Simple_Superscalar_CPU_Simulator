import numpy as np
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
        elif type(decode[4]) is not str:
            r3 = decode[4]
        else:
            r3 = cpu.get_value(decode[4])

        if decode[1] == 0x00: #ADD 
            cpu.WBR[dest] = r2 + r3 
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x01: #SUB
            cpu.WBR[dest] = r2 - r3 
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x02: #MUL
            if self.clock == 1:
                cpu.WBR[dest] = r2 * r3 
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
        elif decode[1] == 0x03: #DIV
            if self.clock == 3:
                cpu.WBR[dest] = int(r2 / r3) if r3 else 0
                cpu.new_dest("R16", self.spec)
                dest = cpu.get_dest("R16")
                cpu.WBR[dest] = r2 %r3
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
        elif decode[1] == 0x04: #XOR
            cpu.WBR[dest] = r2 ^ r3  
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x05: #SHL
            cpu.WBR[dest] = r2 << r3 
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x06: #SHR
            cpu.WBR[dest] = r2 >> r3 
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x07: #CMP
            cpu.WBR[dest] = -1 if r2 < r3 else 0 if r2 == r3 else 1
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()

        elif decode[1] == 0x08:
            length = (cpu.get_length(decode[3]) if cpu.get_length(decode[3]) <=
                      cpu.get_length(decode[4]) else cpu.get_length(decode[4]))
            result = np.array([0]*64)
            result = r2[:length] + r3[:length]
            len_loc = cpu.get_length_location(dest)
            cpu.new_dest(len_loc, self.spec)
            new_len_loc = cpu.get_dest(len_loc) 
            cpu.WBR[new_len_loc] = length
            cpu.WBR[dest] = result
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()

        elif decode[1] == 0x09:
            length = (cpu.get_length(decode[3]) if cpu.get_length(decode[3]) <=
                      cpu.get_length(decode[4]) else cpu.get_length(decode[4]))
            result = np.array([0]*64)
            result = r2[:length] - r3[:length]
            len_loc = cpu.get_length_location(dest)
            cpu.new_dest(len_loc, self.spec)
            new_len_loc = cpu.get_dest(len_loc) 
            cpu.WBR[new_len_loc] = length
            cpu.WBR[dest] = result
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x0A:
            if self.clock == 1:
                length = (cpu.get_length(decode[3]) if cpu.get_length(decode[3]) <=
                          cpu.get_length(decode[4]) else cpu.get_length(decode[4]))
                result = np.array([0]*64)
                result = r2[:length] * r3[:length]
                len_loc = cpu.get_length_location(dest)
                cpu.new_dest(len_loc, self.spec)
                new_len_loc = cpu.get_dest(len_loc) 
                cpu.WBR[new_len_loc] = length
                cpu.WBR[dest] = result
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
        elif decode[1] == 0x0B:
            if self.clock == 2:
                length = (cpu.get_length(decode[3]) if cpu.get_length(decode[3]) <=
                          cpu.get_length(decode[4]) else cpu.get_length(decode[4]))
                vector_1 = r2[:length] 
                vector_2 = r3[:length] 
                cpu.WBR[dest] = int(vector_1.dot(vector_2)) 
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1

        else:
            raise Exception(decode[0] +", " + decode[1] + ": doesn't exist in ALU")
