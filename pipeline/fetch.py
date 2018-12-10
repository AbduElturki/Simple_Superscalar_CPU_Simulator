class fetch_unit(object):
    def __init__ (self, cycle_instruct = 4):
        self.seq_pc = 0x00
        self.tar1_pc = 0x00
        self.cycles = cycle_instruct
        self.speculative = False
    
    def get_target(self, instruct):
        pass

    def fetch(self, cpu):
        branch = lambda x: True  if int(x[:2],16) in range(0x20, 0x28) else False 
        forward = lambda x,y: True if y > x else False

        for cycle in range(self.cycles):
            instruct = self.instruct_cache.popleft() 
            if self.speculative:
                self.instruct_fork["target"].append(instruct)
                instruct = cpu.buf[cpu.seq_pc]
                cpu.pc += 1
                self.instruct_fork["sequential"].append(instruct)
                cpu.seq_pc += 1
            elif branch(instruct):
                cpu.instruct_buf.append(instruct)
                self.speculative = True
            else:
                cpu.instruct_buf.append(instruct)

    def reset(self):
        self.speculative = False
