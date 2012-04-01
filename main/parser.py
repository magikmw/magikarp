#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This object parses and returns input"""

def test():
    from inspect import currentframe, getframeinfo
    file = getframeinfo(currentframe())
    print "Testing {0}".format(file.filename)
    exit("Test complete")

if __name__ == "__main__":
    test()

from log import logg

class Parser():
    def init(self):
        pass

    def ContainsAny(self, str, set):
        """Check whether 'str' contains ANY of the chars in 'set'"""
        for c in set:
            if c in str: return 1
        return 0
