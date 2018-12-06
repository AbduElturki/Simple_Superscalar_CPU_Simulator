class fetch_unit(object):
    def __init__ (self, cycle_instruct = 4):
        self.pc = None
        self.cycles = cycle_instruct
        self.sequential = []
        self.target = []
    
    def jump(self, target):
        if type(target) is not int:
            raise Expectation("Jump target is not int")
        self.pc = target

    def get_target(self, instruct):
        pass

    def fetch(self, cpu):
        branch = lambda x: True  if int(x[:2],16) in range(0x20, 0x28) else False 
        forward = lambda x,y: True if y > x else False

        for cycle in range(self.cycles):
            instruct = cpu.mem[cpu.pc]
            if branch(instruct):
                #TODO
                target = self.get_target(instruct)
                if cpu.branch_predictor.to_take(forward(target,self.pc)):
                    self.instruct_reg = (self.instruct_reg + 1) % 3
                    pass
            else:
                mode = self.seq_target_cache[self.instruct_buf]
                if mode is "target-2":
                    self.instruct_reg["target-2"].append(instruct)
                    self.pc += 1
                    instruct = cpu.mem[cpu.tar1_pc]
                    self.instruct_reg["target-1"].append(instruct)
                    self.tar1_pc += 1
                    instruct = cpu.mem[cpu.seq_pc]
                    self.instruct_reg["sequential"].append(instruct)
                    self.seq_pc += 1
                elif mode is "target-1":
                    self.instruct_reg["target-1"].append(instruct)
                    instruct = cpu.mem[cpu.seq_pc]
                    self.pc += 1
                    self.instruct_reg["sequential"].append(instruct)
                    self.seq_pc += 1
                else:
                    self.instruct_reg["sequential"].append(instruct)
                    self.pc += 1

