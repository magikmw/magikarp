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

# Main imports below
from config import *

class Bot():
    """The main loop class."""

    def __init__(self):
        logg.info('Init: Bot')

    def run(self):
        """Starts the loop"""
        print(NICK)
        print("Bot.run()")
