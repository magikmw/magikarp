#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main loop class file"""

def test():
    from inspect import currentframe, getframeinfo
    file = getframeinfo(currentframe())
    print "Testing {0}".format(file.filename)
    exit("Test complete")

if __name__ == "__main__":
    test()

from log import logg

class Bot():
    """The main loop class."""

    def __init__(self):
        print("Bot imported properly!")

    def run(self):
        print("Bot.run()")
