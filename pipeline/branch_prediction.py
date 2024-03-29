class branch_predictor(object):
    def __init__(self):
        self.forward_state = 1
        self.forward_taken = False 
        self.backward_state = 2
        self.backward_taken = True 

    def to_take(self, forward):
        if forward:
            return self.forward_taken
        else:
            return self.backward_taken

    def update(self, forward, taken):
        if forward:
            print(self.forward_state)
            if taken:
                print("Taken")
                if self.forward_state is 3:
                    self.forward_state = 3
                else:
                    self.forward_state += 1
                    self.forward_taken = True if self.forward_state > 1 else False
            else:
                if self.forward_state is 0:
                    self.forward_state = 0
                else:
                    self.forward_state -= 1
                    self.forward_taken = True if self.forward_state > 1 else False
            print(self.forward_state)
        else:
            if taken:
                if self.backward_state is 3:
                    self.backward_state = 3
                else:
                    self.backward_state += 1
                    self.backward_taken = True if self.backward_state > 1 else False
            else:
                if self.backward_state is 0:
                    self.backward_state = 0
                else:
                    self.backward_state -= 1
                    self.backward_taken = True if self.backward_state > 1 else False
