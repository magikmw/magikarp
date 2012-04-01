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
import datetime
import os

class IrcConnection(object):

    def __init__(self, host, port):
        self.host, self.port = host, port
        self.socket = None
        self.init_connection()
        if not self.socket:
            logg.error("Connection failed to initialise.")
            raise Exception
        else:
            logg.info("Connection established.")

    def init_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.setblocking(0)

    def send_line(self, line):
        self.socket.send(line+"\r\n")

    def receive_lines(self):
        lines = []
        try:
            while(1):
                buffer = self.socket.recv(4096)
                lines += buffer.replace("\r","").split("\n")
        except socket.error as e:
            pass #dammit, I do need to fix this, don't I? Also messages getting cut off.

        return lines

    def get_timestamp(self):
        ret = "["
        ret += datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
        ret += "] "
        return ret

    def close(self):
        self.socket.close()
