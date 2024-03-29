class op_unit(object):
    def __init__(self):
        self.is_loaded =False
        self.decode = None
        self.spec = False
        self.is_busy = False
        self.clock = 0

    def load_decode(self, decode, spec):
        self.spec = spec
        self.decode = decode
        self.is_busy = True
        self.is_loaded = True

    def clear(self):
        self.spec = False
        self.decode = None
        self.is_busy = False
        self.is_loaded = False
        self.clock = 0

    def merge(self):
        if self.is_loaded:
            self.spec = 0

    def flush(self):
        if self.is_loaded and self.spec:
            self.clear()

    def retire_update(self, old, new):
        if self.is_loaded:
            self.decode = [(d.replace(old, new) if type(d) is str else d) for d in self.decode]

    def is_speculative(self):
        return self.spec
