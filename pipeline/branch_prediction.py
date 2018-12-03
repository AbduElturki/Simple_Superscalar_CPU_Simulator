class branch_predictor(object):
    def __init__(self):
        self.state = 2
        self.taken = True

    def to_take(self):
        return self.taken

    def to_stall(self):
        pass

    def update(self, taken):
        if taken:
            if self.state is 3:
                self.state = 3
            else:
                self.state += 1
                self.taken = True if self.state > 1 else False
        else:
            if self.state is 0:
                self.state = 0
            else:
                self.state -= 1
                self.taken = True if self.state > 1 else False

