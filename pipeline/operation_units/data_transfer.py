from .op_unit import op_unit

class data_transfer(op_unit):
    def execute(self, cpu):
        decode = self.decode
        if decode[1] == 0x0: #LD
            if self.clock == 2:
                dest = decode[2]
                MAR = decode[3]
                if dest in cpu.retire_his:
                    dest = cpu.get_value(cpu.retire_his[dest])
                else:
                    dest = cpu.get_value(dest)
                if MAR in cpu.retire_his:
                    MAR = cpu.get_value(cpu.retire_his[MAR])
                else:
                    dest = cpu.get_value(MAR)
                if cpu.is_speculative() and MAR in cpu.spec_mem:
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
                orig = decode[2]
                dest = decode[3]

                if orig in cpu.retire_his:
                    orig = cpu.get_value(cpu.retire_his[dest])
                else:
                    orig = cpu.get_value(dest)

                if dest in cpu.retire_his:
                    MAR = cpu.get_value(cpu.retire_his[dest])
                else:
                    MAR = cpu.get_value(dest)
                if cpu.is_speculative():
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
                    orig = cpu.get_value(cpu.retire_his[dest])
                else:
                    orig = cpu.get_value(dest)

                if dest in cpu.retire_his:
                    MAR = cpu.get_value(cpu.retire_his[dest])
                else:
                    MAR = cpu.get_value(dest)
                if dest in cpu.retire_his:
                    MAR = cpu.get_value(cpu.retire_his[dest])
                else:
                    MAR = cpu.get_value(dest)
                if cpu.is_speculative():
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
                    dest = cpu.get_value(cpu.retire_his[dest])
                else:
                    dest = cpu.get_value(dest)
                if MAR in cpu.retire_his:
                    MAR = cpu.get_value(cpu.retire_his[MAR])
                else:
                    dest = cpu.get_value(MAR)
                if cpu.is_speculative() and MAR in cpu.spec_mem:
                    cpu.WBR[dest] = cpu.spec_mem[MAR + offset]
                else:
                    cpu.WBR[dest] = cpu.mem[MAR + offset]
                cpu.instruct_per_cycle[cpu.cycle] += 1
                self.clear()
            else:
                self.clock += 1
