from __future__ import (print_function)
import os
from struct import (pack, unpack, calcsize)
import math


class CountMinSketch(object):
    ''' Count-Min Sketch class '''

    def __init__(self, width, depth):
        ''' default initilization function '''
        # default values
        self.__width = width
        self.__depth = depth
        self.__elements_added = 0
        # for python2 and python3 support
        self.__int32_t_min = -2147483648
        self.__int32_t_max = 2147483647
        self.__uint64_t_max = 2 ** 64
        self._bins = [0] * (self.__width * self.__depth)
        self._hash_function = self.__default_hash


    def hashes(self, key, depth=None):
        ''' return the hashes for the passed in key '''
        t_depth = self.__depth if depth is None else depth
        return self._hash_function(key, t_depth)

    def put(self, key, num_els=1):
        ''' add an element by using the hashes '''
        hashes = self.hashes(key)
        res = self.__int32_t_max
        for i, val in enumerate(hashes):
            t_bin = (val % self.__width) + (i * self.__width)
            self._bins[t_bin] += num_els
            if self._bins[t_bin] > self.__int32_t_max:
                self._bins[t_bin] = self.__int32_t_max
            if self._bins[t_bin] < res:
                res = self._bins[t_bin]

        self.__elements_added += num_els
        if self.__elements_added > self.__int32_t_max:
            self.__elements_added = self.__int32_t_max

        return res

    def get(self, key):
        ''' check the count-min sketch for an element by using the hashes '''
        hashes = self.hashes(key)
        bins = self.__get_values_sorted(hashes)
        res = bins[0]
        return res


    def __default_hash(self, key, depth):
        ''' the default fnv-1a hashing routine '''
        res = list()
        tmp = key
        for _ in range(0, depth):
            if tmp != key:
                tmp = self.__fnv_1a("{0:x}".format(tmp))
            else:
                tmp = self.__fnv_1a(key)
            res.append(tmp)
        return res

    def __fnv_1a(self, key):
        ''' 64 bit fnv-1a hash '''
        hval = 14695981039346656073
        fnv_64_prime = 1099511628211
        for t_str in key:
            hval = hval ^ ord(t_str)
            hval = (hval * fnv_64_prime) % self.__uint64_t_max
        return hval

    def __get_values_sorted(self, hashes):
        ''' get the values sorted '''
        bins = list()
        for i, val in enumerate(hashes):
            t_bin = (val % self.__width) + (i * self.__width)
            bins.append(self._bins[t_bin])
        bins.sort()
        return bins

