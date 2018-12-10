class fetch_unit(object):
    def __init__ (self, cycle_instruct = 4):
        self.seq_pc = 0x00
        self.tar_pc = 0x00
        self.cycles = cycle_instruct
        self.speculative = False
        self.is_forward = False
    
    def get_target(self, cpu, instruct):
        if int(instruct[:2], 16) is 0x20:
            reg = "R"+str(int(instruct[6:8],16))
            target = cpu.get_value(reg)
        elif int(instruct[:2], 16) is 0x21:
            target = int(instruct[2:], 16) 
        elif int(instruct[:2], 16) is 0x22:
            target = cpu.pc + int(instruct[2:], 16)
        elif int(instruct[:2], 16) is 0x23:
            cpu.new_dest("R14")
            cpu.update_reg("R14", cpu.pc)
            cpu.set_valid("R14")
        elif int(instruct[:2], 16) in range(0x24, 28):
            target = int(instruct[4:], 16)
            pass
        forward = True if target > cpu.pc else False
        return target
        pass

    def fetch(self, cpu):
        branch = lambda x: True  if int(x[:2],16) in range(0x24, 0x28) else False 
        jump = lambda x: True  if int(x[:2],16) in range(0x20, 0x24) else False 
        forward = lambda x: True if cpu.pc < x else False
        if not cpu.is_stalling():
            for cycle in range(self.cycles):
                instruct = self.instruct_cache.popleft() 
                if self.speculative:
                    self.instruct_fork["target"].append(instruct)
                    instruct = cpu.buf[cpu.seq_pc]
                    cpu.tar_pc += 1
                    self.instruct_fork["sequential"].append(instruct)
                    cpu.seq_pc += 1
                elif jump(instruct):
                    cpu.instruct_buf.append(instruct)
                    cpu.pc = get_target(cpu, instruct) 
                elif branch(instruct):
                    cpu.instruct_buf.append(instruct)
                    target = get_target(cpu, instruct) 
                    self.is_forward = forward(target)
                    cpu.speculate(self.is_forward)
                    self.speculative = True
                    self.tar_pc = target 
                else:
                    cpu.instruct_buf.append(instruct)

    def reset(self):
        self.speculative = False
        self.seq_pc = 0x00
        self.tar_pc = 0x00
