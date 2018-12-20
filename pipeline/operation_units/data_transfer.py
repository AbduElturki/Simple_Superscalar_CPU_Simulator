import numpy as np
from .op_unit import op_unit

class data_transfer(op_unit):
    def execute(self, cpu):
        decode = self.decode
        if decode[1] == 0x0: #LD
            if self.clock == 2:
                dest = decode[2]
                MAR = decode[3]
                if dest in cpu.retire_his:
                    dest = cpu.retire_his[dest]
                if MAR in cpu.retire_his:
                    MAR = cpu.get_value(cpu.retire_his[MAR])
                else:
                    MAR = cpu.get_value(MAR)
                if self.spec and MAR in cpu.spec_mem:
                    cpu.WBR[dest] = cpu.spec_mem[MAR]
                else:
                    cpu.WBR[dest] = cpu.mem[MAR]

                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
        elif decode[1] == 0x1: #LDI
            dest = decode[2]
            self.store = False
            cpu.WBR[dest] = decode[3]
            cpu.instruct_per_cycle[cpu.cycle] += 1
            self.clear()
        elif decode[1] == 0x2: #ST
            if self.clock == 1:
                orig = cpu.get_value(decode[2])
                MAR = cpu.get_value(decode[3])
                if self.spec:
                    cpu.spec_mem[MAR] = orig
                else:
                    cpu.mem[MAR] = orig 
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
        elif decode[1] == 0x3: #STO
            if self.clock == 1:
                offset = decode[3]
                orig = decode[2]
                dest = decode[4]

                if orig in cpu.retire_his:
                    orig = cpu.get_value(cpu.retire_his[orig])
                else:
                    orig = cpu.get_value(orig)

                if dest in cpu.retire_his:
                    MAR = cpu.get_value(cpu.retire_his[dest])
                else:
                    MAR = cpu.get_value(dest)
                if dest in cpu.retire_his:
                    MAR = cpu.get_value(cpu.retire_his[dest])
                else:
                    MAR = cpu.get_value(dest)
                if self.spec:
                    cpu.spec_mem[offset + MAR] = orig 
                else:
                    cpu.mem[offset + MAR] = orig 
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
        elif decode[1] == 0x4:
            if self.clock == 2:
                MAR = decode[4]
                offset = decode[3]
                dest = decode[2]
                if dest in cpu.retire_his:
                    dest = cpu.retire_his[dest]
                if MAR in cpu.retire_his:
                    MAR = cpu.get_value(cpu.retire_his[MAR])
                else:
                    MAR = cpu.get_value(MAR)
                if self.spec and MAR in cpu.spec_mem:
                    cpu.WBR[dest] = cpu.spec_mem[MAR + offset]
                else:
                    cpu.WBR[dest] = cpu.mem[MAR + offset]
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
        if decode[1] == 0x5: #VLD
            if self.clock == 2:
                dest = decode[2]
                MAR = decode[3]
                if dest in cpu.retire_his:
                    dest = cpu.retire_his[dest]
                length = cpu.get_length(dest)
                stride = cpu.get_stride(dest)
                end = length * stride
                result = np.array([0]*64)

                if MAR in cpu.retire_his:
                    MAR = cpu.get_value(cpu.retire_his[MAR])
                else:
                    MAR = cpu.get_value(MAR)
                read_from = (range(MAR, (MAR + end)))[::stride]

                if self.spec: 
                    i = 0
                    for addr in read_from:
                        if addr in cpu.spec_mem:
                            result[i] = cpu.spec_mem[addr]
                        else:
                            result[i] = cpu.mem[addr]
                        i += 1
                else:
                    result = cpu.mem[MAR:(MAR+end):stride]
                cpu.WBR[dest] = result

                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
        elif decode[1] == 0x6: #ST
            if self.clock == 1:
                dest = decode[2]
                length = cpu.get_length(dest)
                orig = cpu.get_value(decode[2])
                MAR = cpu.get_value(decode[3])
                store_range = range(MAR, MAR+length)
                if self.spec:
                    raise Exception("")
                    i = 0
                    for addr in store_range:
                        cpu.spec_mem[addr] = orig[i]
                        i += 1
                else:
                    cpu.mem[MAR:(MAR+length)] = orig 
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
