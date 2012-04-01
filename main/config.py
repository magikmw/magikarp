#! /usr/bin/env python2
# -*- coding: utf-8 -*

"""Basic config module

For now contains only constant values but config parsing is planned
Later maybe even an options menu"""

def test():
    from inspect import currentframe, getframeinfo
    file = getframeinfo(currentframe())
    print "Testing {0}".format(file.filename)
    exit("Test complete")

if __name__ == "__main__":
    test()

from log import logg

# Home dir for ''botlinks'' file
from os import getenv

FILEDIR = getenv('USERPROFILE') or getenv('HOME')

DEBUG = True

NICK = 'magiqarp'
NETWORK = 'irc.quakenet.org'
PORT = 6667

if DEBUG == True:
    CHAN = '#mbot'
elif DEBUG == False:
    CHAN = '#rgrd'
