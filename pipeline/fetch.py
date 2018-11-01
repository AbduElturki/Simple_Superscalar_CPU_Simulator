class fetch_unit(object):
    def __init__ (self):
        self.pc = 0
    
    def jump(self, target):
        if type(target) is not int:
            raise Expectation("Jump target is not int")
        self.pc = target

    def fetch(self):
        self.pc += 1
