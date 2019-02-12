#!/usr/bin/env python
# coding: utf-8

# ## Naive implementation of Count-Min sketch




import random
import math
class CountMinSketch:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        self.LONG_PRIME = 4294967311
        self.SOME_RAND=random.random()*(10**8)
        self.countMatrix = [[0]*width for _ in range(depth)]
        self.total=0
        self.hashes=[[0]*2 for _ in range(depth)]
        for i in self.hashes:
            i[0]=int(float(random.random()*(10**8))                     *float(self.LONG_PRIME)/float(self.SOME_RAND) + 1);
            i[1]=int(float(random.random()*(10**8))                     *float(self.LONG_PRIME)/float(self.SOME_RAND) + 1);   
    
    def getHashOfString(self,s):  #hash_djb2                                                                                                        
        hash = 5381
        for x in s:
            hash = (( hash << 5) + hash) + ord(x)
        return hash & 0xFFFFFFFF
    
    def update(self,item, size):
        self.total+=size
        hashval=0
        hashed_item=self.getHashOfString(item)
        for j in range(self.depth):
            hashval = ((self.hashes[j][0]*hashed_item                         + self.hashes[j][1])%self.LONG_PRIME)%self.width
            self.countMatrix[j][hashval]+=size
    
    def estimate(self,item):
        minval=math.inf
        hashval=0
        hashed_item=self.getHashOfString(item)
        for j in range(self.depth):
            hashval = ((self.hashes[j][0]*hashed_item                         + self.hashes[j][1])%self.LONG_PRIME)%self.width
            minval = min(minval,self.countMatrix[j][hashval])
        return minval


















































