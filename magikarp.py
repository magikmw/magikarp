#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import socket

DEBUG = True

NICK = 'magikarp'
NETWORK = 'irc.quakenet.org'
PORT = 6667

if DEBUG == True:
    CHAN = '#mbot'
elif DEBUG == False:
    CHAN = '#rgrd-ot'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

irc.connect((NETWORK,PORT))

#receive buffer, and connect setup
irc.recv(4096) #rcv buffer
irc.send('NICK ' + NICK + '\r\n')
irc.send('USER magikarp magikarp magikarp :magikarp\r\n')

while True:
    data = irc.recv(4096)
    print(data)
    if data.find('MODE ' + NICK + ' +i') != -1:
        irc.send('JOIN ' + CHAN + '\r\n')
        irc.send('PRIVMSG ' + CHAN + ' :Morning, ' + CHAN + '\r\n')
        False
    if data.find('PING') != -1:
        irc.send('PONG ' + data.split()[1] + '\r\n')

while True:
    if data.find('PING') != -1:
        irc.send('PONG ' + data.split()[1] + '\r\n')
