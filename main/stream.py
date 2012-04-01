#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Datastream object file"""

def test():
    from inspect import currentframe, getframeinfo
    file = getframeinfo(currentframe())
    print "Testing {0}".format(file.filename)
    exit("Test complete")

if __name__ == "__main__":
    test()

from log import logg

import socket

Stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
