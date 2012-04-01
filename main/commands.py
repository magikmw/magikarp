#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file contains all the commands recognizable by the parser."""

def test():
    from inspect import currentframe, getframeinfo
    file = getframeinfo(currentframe())
    print "Testing {0}".format(file.filename)
    exit("Test complete")

if __name__ == "__main__":
    test()

from log import logg
