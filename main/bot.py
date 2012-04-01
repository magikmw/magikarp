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

from config import *
from stream import Stream
from parser import Parser
import misc as Misc

from time import altzone

class Bot():
    """The main loop class."""

    def __init__(self):
        logg.info('Init: Bot')

    def run(self):
        """Starts the loop"""
        print(NICK)
        print("Bot.run()")

        Stream.connect((NETWORK,PORT))
        #receive buffer, and connect setup
        Stream.recv(4096) #rcv buffer
        Stream.send('NICK ' + NICK + '\r\n')
        Stream.send('USER magikarp magikarp magikarp :magikarp\r\n')

        # main loop
        while True:
            data = Stream.recv(4096) # get lines
            print(data) #print lines

            # Basic init commands after server connection
            if data.find('MODE ' + NICK + ' +i') != -1:
                Stream.send('JOIN ' + CHAN + '\r\n')
                #Stream.send('PRIVMSG ' + CHAN + ' :Morning, ' + CHAN + '\r\n')

            # Constant ping lookout
            if data.find('PING') != -1:
                Stream.send('PONG ' + data.split()[1] + '\r\n')

            elif data.find('PRIVMSG') != -1: #if there is a PRIVMSG in data then parse it
                message = ':'.join(data.split(':')[2:]) #split the command from the message
                print(message)

                function = message.split( )[0] #split the massage to get function name

                if message.lower().find('awesome') != -1 and not function.find('^') != -1: #split the massage to get function name:
                    nick = data.split('!')[ 0 ].replace(':','') #snatch the nick issuing the command
                    destination = ''.join (data.split(':')[:2]).split (' ')[-2]
                    #Stream.send('PRIVMSG ' + destination + ' :Yeah ' + nick + '! Awesome!\r\n')

                if Parser().ContainsAny(message, ['http', 'http', 'www', '.com', '.org', '.eu']) == 1:
                    nick = data.split('!')[ 0 ].replace(':','') #snatch the nick issuing the command
                    destination = ''.join (data.split(':')[:2]).split (' ')[-2]
                    arg = data.split( )
                    args = []
                    for index,item in enumerate(arg): #for every index and item in arg
                        if index > 2 and Parser().ContainsAny(item, ['http', 'http', 'www', '.com', '.org', '.eu']) == 1:
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
                        Stream.send('PRIVMSG ' + destination + ' :' + nick + ": I'm developed by magikmw - http://github.com/magikmw/magikarp \r\n")

                    elif function == '^say':
                        if args != '':
                            #Stream.send('PRIVMSG ' + destination + ' :' + args + '\r\n')
                            Stream.send('PRIVMSG ' + destination + " : I'm sorry " + nick + ", but I cannot let you do that.\r\n")
                        else:
                            Stream.send('PRIVMSG ' + destination + ' : What do you want me to say, ' + nick + '?\r\n')

                    elif function == '^time':
                        tz = altzone / 60 / 60
                        tz = tz * -1
                        if tz < 0:
                            tz = '+' + str(tz)
                        elif tz > 0:
                            tz = '-' + str(abs(tz))
                        elif tz == 0:
                            tz = ''
                        Stream.send('PRIVMSG ' + destination + ' :' + nick + ': The current time is: ' + Misc.CurrentTimeString() + ' GMT' + str(tz) +'\r\n')
