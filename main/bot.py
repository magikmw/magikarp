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

import connection

from config import *
from parser import Parser
import misc as Misc

from time import altzone

class Bot():
    """The main loop class."""

    def __init__(self, host, port, user, realname, nick, debug=True):
        logg.info('Init: Bot')
        self.host = host
        self.port = port
        self.user = user
        self.realname = realname
        self.nick = nick
        self.debug = debug
        self.quitting = False
        self.init()

    def init(self):
        self.connection = connection.IrcConnection(self.host, self.port)
        self.send_init()
        return self.handle_input()

    def send_init(self):
        self.change_nick(self.nick)
        self.send_raw_line('USER '+self.nick+' '+self.user+' '+self.user+' :'+self.realname)
        print("send_int sent")

    def send_raw_line(self, line):
        self.connection.send_line(line)

    def send_chan_line(self, channel, line):
        self.send_raw_line("PRIVMSG "+channel.strip()+" :"+line)

    def send_priv_line(self, target, line):
        self.send_raw_line("PRIVMSG "+target.strip()+" :"+line)
        # yes, I know it's the same

    def part_channel(self, channel, reason="No reason given."):
        self.send_raw_line("PART "+channel+" :"+reason)

    def set_self_mode(self, flags):
        self.send_raw_line("MODE "+self.nick+" :"+flags)

    def set_chan_mode(self, channel, flags):
        self.send_raw_line("MODE "+channel+" :"+flags)

    def quit(self, reason="No reason given."):
        self.quitting = True
        self.send_raw_line("QUIT :"+reason)
        self.connection.close()

    def change_nick(self, new_nick):
        self.nick = new_nick
        self.send_raw_line('NICK '+self.nick)

    def join_channel(self, channel):
        self.send_raw_line('JOIN '+channel)

    def handle_input(self):
        lines = self.connection.receive_lines()
        if lines != "":
            for line in lines:
                self.handle_raw_line(line)
            return 0
        else:
            return 1

    def handle_raw_line(self, line):
        if self.debug == True:
            print(line)
        if line.startswith("PING"):
            print("got ping!")
            self.send_raw_line("PONG "+line.replace("PING ",""))
        elif line.startswith(":"):
            #we assume command is the bits between colons, if there are at least two, else whole line
            command = line[1:]
            if line.count(":")>1:
                command = line[1:].split(":",1)[0]

            if " PRIVMSG " in command:
                #it's a privmsg
                tmp, target = command.split(" PRIVMSG ",1)
                nick, host = tmp.split("!",1)
                message = line[1:].split(":",1)[1]
                if self.nick not in target:
                    self.handle_chan_msg(nick, host, target, message)
                else:
                    self.handle_priv_msg(nick, host, message)
            elif " JOIN " in command:
                #it's a join notification
                tmp, channel = line.split(" JOIN ",1)
                nick, host = tmp[1:].split("!",1)
                channel = "#" + channel.split("#",1)[1] #fix for missing join :'s in some ircds
                self.handle_join(nick, host, channel)
            elif " PART " in command:
                #it's a part notification
                tmp, channel = line.split(" PART ",1)
                nick, host = tmp[1:].split("!",1)
                channel = "#" + channel.split("#",1)[1] #fix for missing part :'s in some ircds
                self.handle_part(nick, host, channel)
            elif " MODE " in command:
                #it's a mode change
                origin, target = command.split(" MODE ",1)
                if self.nick in origin and self.nick in target:
                    flags = line[1:].split(":",1)[0]
                    op = "+"
                    for flag in flags:
                        if flag == " ":
                            break
                        elif flag in ("+", "-"):
                            op = flag
                        else:
                            self.handle_self_mode(op + flag)
                else:
                    nick, host = origin.split("!", 1)
                    chan, flags = target.split(" ",1)
                    flags = flags.replace(":","").strip()
                    op = None
                    for flag in flags:
                        if flag == " ":
                            break
                        elif flag in ("+","-"):
                            op = flag
                        else:
                            self.handle_chan_mode(nick, host, chan, op + flag)
        if line.count("End of /MOTD"):
            self.end_of_motd()

    def handle_chan_msg(self, nick, host, channel, msg):
        channel = channel.strip()
        if self.debug:
            print("Got channel message: <"+nick+channel+"> "+msg)

    def handle_priv_msg(self, nick, host, msg):
        if self.debug:
            print("Got private message: <"+nick+"@"+host+"> "+msg)

    def handle_join(self, nick, host, channel):
        if self.debug:
            print(nick +" joined "+channel+".")

    def handle_part(self, nick, host, channel):
        if self.debug:
            print(nick +" has left "+channel+".")

    def handle_self_mode(self, mode):
        if self.debug:
            print("Set mode on self: "+mode)

    def handle_chan_mode(self, nick, host, channel, mode):
        channel = channel.strip()
        if self.debug:
            print("Set mode on channel "+channel+": "+mode)

    def end_of_motd(self):
        self.set_self_mode("+B")

    def debug_log(self, line):
        self.connection.debug_log(line)

    def update(self):
        err = self.handle_input()
        while err and not quitting:
            if self.log:
                self.connection.error_log("Disconnected from server. Reconnecting.. ")
            time.sleep(5)
            err = self.init()

    def end_of_motd(self):
        for chan in CHANNELS:
            self.join_channel(chan)

    def handle_priv_msg(self, nick, host, msg):
        auth = self.get_auth(nick, host, None)
        if msg.startswith("join") and auth == 2:
            chan = msg.split(" ",1)[1]
            self.join_channel(chan)

    def handle_chan_msg(self, nick, host, chan, msg):
        #first, test for some basic commands.
        if msg.startswith("."):
            #it's a command, let's pass the call down the line.
            self.handle_command(nick, host, chan, msg[1:])
        else:
            #it's not a command, it's just chatter.
            pass

# from here on are methods only for this subclass

    def handle_command(self, nick, host, chan, cmd):
        #we just got a bot command.
        auth = self.get_auth(nick, host, chan)
        if cmd.startswith("quit") and auth == 2:
            if " " in cmd:
                self.quit(cmd.split(" ",1)[1])
            else:
                self.quit()
        elif cmd.startswith("part") and auth:
            self.part_channel(chan)
        elif cmd.startswith("docs"):
            line = "My github page is available at: "+GITHUB
            self.send_priv_line(nick, line)

    def get_auth(self, nick, host, chan):
        """Returns a level of authentication for the nick, depending on the nick,
the host, and the channel it's about. This allows per-channel auths."""
        if nick == OWNER: #for debugging, mostly. This should be host-based.
            return 2 # Global authentication for author.
        else:
            return 0 # No admin capabilities, only standard permissions.
