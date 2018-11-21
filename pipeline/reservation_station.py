import pandas as pd

class reservation_station(object):
    def __init__(self, size):
        self.size = size
        self.reservation = pd.DataFrame({'busy' : [False] * size,
                                         'opcode' : [0x00] * size,
                                         'vj' : [0x00] * size,
                                         'vk' : [0x00] * size,
                                         'qj' : [0x00] * size,
                                         'qk' : [0x00] * size,
                                         'a'  : [0x00] * size
                                        })

    def is_free_space(self):
        return (self.reservation['busy'] == False).any()
