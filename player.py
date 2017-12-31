# Yichen Zhou (yz793)

import socket
import threading
import sys
import json
import os
import struct

DEBUG_MODE = True
CMD_PREFIX = "Picture"

TYPE_REGISTER_GAME = "register game"
TYPE_JOIN_GAME = "join game"
TYPE_ACK = "acknowledge"
TYPE_DISPLAY = "display"
TYPE_REGISTER_AVATAR = "register avatar"

def debuglog(outstr):
    if DEBUG_MODE:
        print("DEBUG> " + outstr)

def println(outstr):
    print(CMD_PREFIX + "> " + outstr)

def readln(outstr=None):
    if outstr is not None:
        println(outstr) 
    return input(CMD_PREFIX + "> ")

class Player:
    def __init__(self, address=None, port=None, alias=None, table=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = b''
        print("Platform of Indirect Competition of Tabletop Unsupervised Recreational Efficiency v.1")
        while True:
            self.address = readln("Input server address.") if address is None else address
            self.port = eval(readln("Input server port.")) if port is None else port

            println("Connecting to server.")
            self.socket.connect((self.address, self.port))
            println("Connected.")

            msg = self.listen()
            if msg["type"] == TYPE_DISPLAY:
                println("Display info:\n" + msg["info"] + "\n")
                
            self.alias = readln("Register your alias.") if alias is None else alias
            self.table = readln("Join which table.") if table is None else table
            self.speak({
                "type": TYPE_JOIN_GAME,
                "alias": self.alias,
                "table": eval(self.table)
                })
            if self.awaitAck():
                println("Joined game.")
                while True:
                    msg = self.listen()
                    println(json.dumps(msg))

    def listen(self):
        while True:
            data = self.socket.recv(8192)
            if not data:
                return None
            self.buffer += data

            while len(self.buffer) >= 4:
                msgLen = struct.unpack(">I", self.buffer[0:4])[0]
                self.buffer = self.buffer[4:]
                while len(self.buffer) < msgLen:
                    data = self.socket.recv(8192)
                    if not data:
                        return None
                    self.buffer += data

                msg = self.buffer[:msgLen].decode()
                self.buffer = self.buffer[msgLen:]
                msg = json.loads(msg)["content"]
                return msg

    def awaitAck(self):
        msg = self.listen()
        return True if msg["type"] == TYPE_ACK else False

    def speak(self, content):
        data = {"content": content}
        msg = json.dumps(data).encode()
        self.socket.sendall(struct.pack(">I", len(msg)) + msg)

    def ack(self):
        self.speak({"type": TYPE_ACK})

if __name__ == "__main__":
    Player()

