class reservation(object):
    def __init__(self, oc, source_1=None, valid_1=True, source_2=None, valid_2=True, destination=None):
        self.oc = oc
        self.source_1 = source_1
        self.source_2 = source_2
        self.valid_1 = valid_1
        self.valid_2 = valid_2
        self.destination = destination
        
