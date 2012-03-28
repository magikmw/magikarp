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
    data = irc.recv(4096) # get lines
    print(data) #print lines

    # Basic init commands after server connection
    if data.find('MODE ' + NICK + ' +i') != -1:
        irc.send('JOIN ' + CHAN + '\r\n')
        irc.send('PRIVMSG ' + CHAN + ' :Morning, ' + CHAN + '\r\n')

    # Contant ping lookout
    if data.find('PING') != -1:
        irc.send('PONG ' + data.split()[1] + '\r\n')

    elif data.find('PRIVMSG') != -1: #if there is a PRIVMSG in data then parse it
        print('PRIVMSG')
        message = ':'.join(data.split(':')[2:]) #split the command from the message
        print(message)

        function = message.split( )[0] #split the massage to get function name

        if message.lower().find('awesome') != -1 and not function.find('.') != -1: #split the massage to get function name:
            nick = data.split('!')[ 0 ].replace(':',' ') #snatch the nick issuing the command
            destination = ''.join (data.split(':')[:2]).split (' ')[-2]
            irc.send('PRIVMSG ' + destination + ' : Yeah ' + nick + '! Awesome!\r\n')

        if message.lower().find('.') != -1: #if the message contains the chan name
            nick = data.split('!')[ 0 ].replace(':',' ') #snatch the nick issuing the command
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

            if function == '.credits': #if function is equal to .credits
                irc.send('PRIVMSG ' + destination + ' :' + nick + ': I was coded by magikmw\r\n')

            if function == '.say':
                if args != '':
                    irc.send('PRIVMSG ' + destination + ' :' + args + '\r\n')
                else:
                    irc.send('PRIVMSG ' + destination + ' : What do you want me to say, ' + nick + '?\r\n')
