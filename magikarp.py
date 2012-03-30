#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A simple IRCbot

Created with various tutorial I've found on the internets
by Michał Walczak
"""

"""
DEVNOTES
[TODO] ^weather command
[TODO] ^quit, ^join commands
[TODO] ^changename command
[TODO] Link grab toggle per channel
[XXX] Make parsing better (check http://www.osix.net/modules/article/?id=780)
[XXX] OOP the thing, make plugin components possible
[TODO] Comment the code
[TODO] Readme, document the commands
[TODO] Config file
[TODO] Runtime command line (basically an IRC client functionality).
"""

import sys, getopt

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere

if __name__ == "__main__":
    main()
    from main import Bot
    Bot().run()
else:
    print("This module is not importable.")

