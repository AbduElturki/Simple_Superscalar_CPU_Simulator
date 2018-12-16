class fetch_unit(object):
    def __init__ (self, cycle_instruct = 4):
        self.seq_pc = 0x00
        self.tar_pc = 0x00
        self.cycles = cycle_instruct
        self.speculative = False
        self.is_forward = False
    
    def get_target(self, cpu, instruct, jal=False):
        op = int(instruct[:2],16)
        if op == 0x20:
            reg = "R"+str(int(instruct[6:8],16))
            target = cpu.get_value(reg)
        elif op == 0x21:
            target = int(instruct[2:], 16) 
        elif op == 0x22:
            target = cpu.pc + int(instruct[2:], 16)
        elif op == 0x23:
            if jal:
                cpu.new_dest("R14", True)
                cpu.update_reg("R14", cpu.pc)
                cpu.set_valid("R14")
        elif op in range(0x24, 0x28):
            target = int(instruct[4:], 16)
        else:
            raise Exception("get_target")
        return target

    def fetch(self, cpu):
        branch = lambda x: True  if int(x[:2],16) in range(0x20, 0x28) else False 
        jump = lambda x: True  if int(x[:2],16) in range(0x20, 0x24) else False 
        forward = lambda x: True if cpu.pc < x else False
        if not cpu.is_stalling():
            for cycle in range(self.cycles):
                if cpu.pc == len(cpu.instruct_cache): 
                    break
                if self.speculative:
                    if not self.tar_pc == len(cpu.instruct_cache):
                        instruct = cpu.instruct_cache[self.tar_pc]
                        if (not branch(instruct) and not
                            (len(cpu.instruct_fork['target']) == 8)):
                            cpu.instruct_fork["target"].append(instruct)
                            if jump(instruct):
                                jal = cpu.speculate_mode() is "target"
                                self.tar_pc = self.get_target(cpu, instruct, jal)
                            else:
                                self.tar_pc += 1
                    if not self.seq_pc == len(cpu.instruct_cache):
                        instruct = cpu.instruct_cache[self.seq_pc]
                        if (not branch(instruct) and not
                            (len(cpu.instruct_fork['sequential']) == 8)):
                            cpu.instruct_fork["sequential"].append(instruct)
                            if jump(instruct):
                                jal = cpu.speculate_mode() is "sequential"
                                self.seq_pc = self.get_target(cpu, instruct)
                            else:
                                self.seq_pc += 1
                else:
                    instruct = cpu.instruct_cache[cpu.pc]
                    if jump(instruct):
                        cpu.instruct_buffer.append(instruct)
                        cpu.pc = self.get_target(cpu, instruct) 
                    elif branch(instruct):
                        cpu.branching += 1
                        cpu.instruct_buffer.append(instruct)
                        target = self.get_target(cpu, instruct) 
                        self.is_forward = forward(target)
                        cpu.speculate(self.is_forward)
                        self.speculative = True
                        self.tar_pc = target 
                        self.seq_pc = cpu.pc + 1
                        
                    else:
                        cpu.instruct_buffer.append(instruct)
                    cpu.pc_increment()

    def merge(self, cpu):
        if cpu.speculate_mode() is "sequential":
            cpu.pc = self.seq_pc
        elif cpu.speculate_mode() is "target":
            cpu.pc = self.tar_pc
        else:
            raise Exception("Unkown spec state")

    def flush(self, cpu):
        if cpu.speculate_mode() is "sequential":
            cpu.pc = self.tar_pc
        elif cpu.speculate_mode() is "target":
            cpu.pc = self.seq_pc
        else:
            raise Exception("Unkown spec state")

    def reset(self):
        self.speculative = False
        self.seq_pc = 0x00
        self.tar_pc = 0x00
