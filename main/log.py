#! /usr/bin/env python2
# -*- coding: utf-8 -*-

"""Debug loging function"""

def test():
    from inspect import currentframe, getframeinfo
    file = getframeinfo(currentframe())
    print "Testing {0}".format(file.filename)
    exit("Test complete")

if __name__ == "__main__":
    test()

import logging

# create a logger
logg = logging.getLogger('Main')
logg.setLevel(logging.DEBUG)

# create a handler and set level
logg_ch = logging.StreamHandler()
logg_fh = logging.FileHandler('debug.log', mode='a', encoding=None, delay=False
)
logg_ch.setLevel(logging.INFO)
logg_fh.setLevel(logging.DEBUG)

# crate a formatter and add it to the handler
# [HH:MM:SS AM][LEVEL] Message string
logg_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%I:%M:%S')
logg_ch.setFormatter(logg_formatter)
logg_fh.setFormatter(logg_formatter)

# add ch to logger
logg.addHandler(logg_ch) #console handler at level INFO
logg.addHandler(logg_fh) #file handler at level DEBUG for more detail

# ready to go!
# logging convention:
# logg.debug('') for variable passing
# logg.info('') for standard initialization messages
# logg.warn('') for known errors and caught exceptions
# logg.error('') for something that shouldn't happen
# logg.critical('') for breakage errors

logg.info('Logging initialized.')

