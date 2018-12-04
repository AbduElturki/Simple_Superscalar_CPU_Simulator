class op_unit(object):
    def __init__(self):
        self.is_loaded =False
        self.decode = None
        self.is_busy = False
        self.clock = 0

    def load_decode(self, decode):
        self.decode = decode
        self.is_busy = True
        self.is_loaded = True

    def clear(self):
        self.decoe = None
        self.is_busy = False
        self.is_loaded = False
