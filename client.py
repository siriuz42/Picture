# Yichen Zhou (yz793)

import socket
import threading
import sys
import json
import os

MAX_PLAYER_NUM = 32
TIME_OUT_THRESH = 10
DEBUG_MODE = True

CMD_PREFIX = "Picture"

CMD_CONNECT = "connect"
CMD_ERROR = "error"
CMD_HELP = "help"
CMD_LINK = "link"
CMD_READY = "ready"
CMD_ALIAS = "alias"
CMD_JOIN = "join"

def debuglog(str):
    if DEBUG_MODE:
        print "DEBUG> ", str

def readln():
    return raw_input(CMD_PREFIX + "> ")

def println(outstr):
    print CMD_PREFIX + "> " + outstr

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.alias = None

    def listen(self):
        

    def cmdParser(self, cmd):
        cmd = cmd.rstrip()
        ret = {"cmd": CMD_ERROR}
        try:
            ## Help
            if cmd.startswith(CMD_HELP):
                pass
            ## Connect
            elif cmd.startswith(CMD_CONNECT):
                wSplit = cmd.find(" ", len(CMD_CONNECT)+1)
                ret["cmd"] = CMD_CONNECT
                ret["address"] = cmd[len(CMD_CONNECT)+1:wSplit]
                ret["port"] = eval(cmd[wSplit+1:])
            ## Ready
            elif cmd.startswith(CMD_READY):
                ret["cmd"] = CMD_READY
            ## Link
            elif cmd.startswith(CMD_LINK):
                ret["cmd"] = CMD_LINK
                ret["file"] = cmd[len(CMD_LINK)+1:]
            ## Alias
            elif cmd.startswith(CMD_ALIAS):
                ret["cmd"] = CMD_ALIAS
                ret["alias"] = cmd[len(CMD_ALIAS)+1]
            ## Join
            elif cmd.startswith(CMD_JOIN):
                ret["cmd"] = CMD_JOIN
                ret["table"] = cmd[len(CMD_JOIN)+1:]
        except:
            return {"cmd": CMD_ERROR}
        else:
            return ret

    def cmdRun(self, cmd):
        cmdParsed = self.cmdParser(cmd)
        ## Error
        if cmdParsed["cmd"] == CMD_ERROR:
            println("Unable to process command.")
            return 0
        ## Connect
        elif cmdParsed["cmd"] == CMD_CONNECT:
            self.socket.connect((cmdParsed["address"], cmdParsed["port"]))
            self.socket.send("Initialize connection.")
        ## 

    def kickoff(self):
        while True:
            cmd = readln()
            self.cmd = self.cmdParser(cmd)
            self.cmdRun(self.cmd)

if __name__ = "__main__":
    print "Platform for Indirect Competition of Tabletop Ultimate Recreational Entertainment v1.0"
    client = Client()
    client.kickoff()






