#! /usr/bin/env python2
# -*- coding: utf-8 -*-

"""Simple bot created with various IRC bot tutorials I've found on the web.
Docs to be created yet"""

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
[TODO] Runtime command line.
"""

import socket
from os import getenv
from datetime import datetime
from time import altzone

FILEDIR = getenv('USERPROFILE') or getenv('HOME')

def ContainsAny(str, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    for c in set:
        if c in str: return 1
    return 0

def CurrentTimeString():
    now = datetime.now()
    string = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute)
    return string

DEBUG = False

NICK = 'magiqarp'
NETWORK = 'irc.quakenet.org'
PORT = 6667

if DEBUG == True:
    CHAN = '#mbot'
elif DEBUG == False:
    CHAN = '#rgrd'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

irc.connect((NETWORK,PORT))

#receive buffer, and connect setup
irc.recv(4096) #rcv buffer
irc.send('NICK ' + NICK + '\r\n')
irc.send('USER magikarp magikarp magikarp :magikarp\r\n')

while True:
    data = irc.recv(4096) # get lines
    print(data) #print lines

    # Basic init commands after server connection
    if data.find('MODE ' + NICK + ' +i') != -1:
        irc.send('JOIN ' + CHAN + '\r\n')
        #irc.send('PRIVMSG ' + CHAN + ' :Morning, ' + CHAN + '\r\n')

    # Constant ping lookout
    if data.find('PING') != -1:
        irc.send('PONG ' + data.split()[1] + '\r\n')

    elif data.find('PRIVMSG') != -1: #if there is a PRIVMSG in data then parse it
        message = ':'.join(data.split(':')[2:]) #split the command from the message
        print(message)

        function = message.split( )[0] #split the massage to get function name

        if message.lower().find('awesome') != -1 and not function.find('^') != -1: #split the massage to get function name:
            nick = data.split('!')[ 0 ].replace(':',' ') #snatch the nick issuing the command
            destination = ''.join (data.split(':')[:2]).split (' ')[-2]
            irc.send('PRIVMSG ' + destination + ' :Yeah ' + nick + '! Awesome!\r\n')

        if ContainsAny(message, ['http', 'http', 'www', '.com', '.org', '.eu']) == 1:
            nick = data.split('!')[ 0 ].replace(':',' ') #snatch the nick issuing the command
            destination = ''.join (data.split(':')[:2]).split (' ')[-2]
            arg = data.split( )
            args = []
            for index,item in enumerate(arg): #for every index and item in arg
                if index > 2 and ContainsAny(item, ['http', 'http', 'www', '.com', '.org', '.eu']) == 1:
                    n=1
                    if args == []:
                        #item = (item.split(':', 1)[1])
                        args.append(item)
                    else:
                        args.append(' ' + item)
                        n += 1

            args.append('\n')
            print args

            if args != '':
                fileObj = open(FILEDIR + "/botlinks", "a")
                fileObj.write('['+destination+'] '+ CurrentTimeString() + ' ' + nick + ': ')
                for i in args:
                    fileObj.write(i)
                fileObj.close()

        if message.lower().find('^') != -1: #if the message contains the chan name
            nick = data.split('!')[ 0 ].replace(':','') #snatch the nick issuing the command
            print('nick: ' + nick)
            destination = ''.join (data.split(':')[:2]).split (' ')[-2]
            print('dest: ' + destination)
            function = message.split( )[0] #split the massage to get function name
            print('function: ' + function)
            print('The function called is ' + function + ' from ' + nick) #command and the caller
            arg = data.split( ) # arg[0] is the actual comand

            args = ''
            for index,item in enumerate(arg): #for every index and item in arg
                if index > 3:
                    if args == '':
                        args = item
                    else:
                        args += ' ' + item
            print(args)

            if function == '^credits': #if function is equal to ^credits
                irc.send('PRIVMSG ' + destination + ' :' + nick + ": I'm developed by magikmw - http://github.com/magikmw/magikarp \r\n")

            elif function == '^say':
                if args != '':
                    #irc.send('PRIVMSG ' + destination + ' :' + args + '\r\n')
                    irc.send('PRIVMSG ' + destination + " : I'm sorry " + nick + ", but I cannot let you do that.\r\n")
                else:
                    irc.send('PRIVMSG ' + destination + ' : What do you want me to say, ' + nick + '?\r\n')

            elif function == '^time':
                tz = altzone / 60 / 60
                tz = tz * -1
                if tz < 0:
                    tz = '+' + str(tz)
                elif tz > 0:
                    tz = '-' + str(abs(tz))
                elif tz == 0:
                    tz = ''
                irc.send('PRIVMSG ' + destination + ' :' + nick + ': The current time is: ' + CurrentTimeString() + ' GMT' + str(tz) +'\r\n')
