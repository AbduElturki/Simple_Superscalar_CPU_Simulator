class write_back(object):
    def __init__(self):
        self.mode = None 
        self.decode = None 
        self.buf = None 
    
    def write_back(self, mode, decode, buf, reg):
        self.mode = mode
        self.decode = decode
        self.buf = buf
        if self.mode is "ALU":
            destination = decode[1]
            reg[destination] = self.buf
        else:
            pass

