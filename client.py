# Yichen Zhou (yz793)

import socket
import threading
import sys
import json
import os

MAX_PLAYER_NUM = 32
TIME_OUT_THRESH = 10
DEBUG_MODE = True

CMD_HELP = 
CMD_CONNECT = "connect"
CMD_SEAT = "seat"
CMD_ERROR = "error"


CMD_PREFIX = "Picture"

def debuglog(str):
    if DEBUG_MODE:
        print "DEBUG> ", str

def readln():
    return raw_input(CMD_PREFIX + "> ")

def println(outstr):
    print CMD_PREFIX + "> " + outstr

if __name__ = "__main__":
    print "Platform for Indirect Competition of Tabletop Ultimate Recreational Entertainment v1.0"
    while True:
        cmd = readln()
        cmdParsed = cmdParser(readln())
        if cmdParsed["cmd"] = "error"
        







