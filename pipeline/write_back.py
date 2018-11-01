class write_back(object):
    def __init__(self, mode, decode, buf):
        self.mode = mode
        self.decode = decode
        self.buf = buf
    
    def write_back(self, reg):
        if self.mode is "ALU":
            destination = decode[1]
            reg[destination] = self.buf
        else:
            pass

