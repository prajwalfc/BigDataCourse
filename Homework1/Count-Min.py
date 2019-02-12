class CountMinSketch:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        self.countMatrix = [[0] * width] * depth
        # self.hashes=getHashes(self.depth)

    def getHashOfString(self,
                        s):  # hash_djb2
        hash = 5381
        for x in s:
            hash = ((hash << 5) + hash) + ord(x)
        return hash & 0xFFFFFFFF

c=CountMinSketch(7,4)
c.countMatrix