class fetch_unit(object):
    def __init__ (self):
        self.pc = None
    
    def jump(self, target):
        if type(target) is not int:
            raise Expectation("Jump target is not int")
        self.pc = target

    def fetch(self, cpu):
        cpu.update_instruct_reg()
        cpu.pc_increment()
        self.pc = cpu.pc
