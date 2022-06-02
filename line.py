class Line:
    def __init__(self, size):
        self.data = [0] * size # data bits 
        self.valid = 0 # valid bit 
        self.tag = 0 # tag 
        self.use = 0 # for lru tracking
        self.modified = 0 # bit set if Line modified 
