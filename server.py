# Yichen Zhou (yz793)

import socket
import threading
import sys
import json
import os
import struct

MAX_TABLE = 32

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

class Table:
    def __init__(self, judge, game, alias):
        # player 0 is always the judge
        self.players = [judge]
        self.game = game
        self.judgeAlias = alias
        self.status = "Waiting"

    def broadcast(self, msg):
        for player in self.players:
            player.speak(msg)

    def whisper(self, msg, recipient):
        # recipient 0 is always the judge
        self.players[recipient].speak(msg)

class Casino:
    def __init__(self):
        self.tables = []

    def newTable(self, judge, game, alias):
        table = Table(judge, game, alias)
        self.tables.append(table)
        return table

    def flushInfo(self):
        ret = "Table\tGame\tJudge\tPlayer\tStatus"
        for i in range(len(self.tables)):
            table = self.tables[i]
            ret += "\n" + str(i) + "\t" + table.game + "\t" + table.judgeAlias + "\t" + str(len(table.players)-1) + "\t" + table.status
        return ret

class Avatar(threading.Thread):
    def __init__(self, socket, casino):
        threading.Thread.__init__(self)
        self.casino = casino
        self.socket = socket
        self.alias = "Anonymous"
        self.buffer = b''
        self.speak({
            "type": TYPE_DISPLAY,
            "info": self.casino.flushInfo()
            })

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

    def speak(self, content):
        data = {"content": content}
        msg = json.dumps(data).encode()
        self.socket.sendall(struct.pack(">I", len(msg)) + msg)

    def ack(self):
        self.speak({"type": TYPE_ACK})

    def run(self):
        while True:
            msg = self.listen()
            if msg is not None:
                if msg["type"] == TYPE_REGISTER_GAME:
                    self.alias = self.alias if msg["alias"] is None else msg["alias"]
                    self.table = self.casino.newTable(self, msg["game"], self.alias)
                    self.ack()
                elif msg["type"] == TYPE_JOIN_GAME:
                    self.alias = self.alias if msg["alias"] is None else msg["alias"]
                    self.table = self.casino.tables[msg["table"]]
                    self.table.players.append(self)
                    self.ack()
                    self.table.broadcast({
                        "type": TYPE_DISPLAY,
                        "info": "A new player joined game. " + str(len(self.table.players)-1)+ " players waiting."
                        })
                else:
                    println(msg)

class Manager:
    def __init__(self, address, port):
        try:
            self.casino = Casino()
            self.table = {}
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            println("Creating server.")
            self.socket.bind((address, eval(port)))
            self.socket.listen(5)
            println("Created server. Begin to listen.")
        except:
            println("Failure during initialization.")
            return 
        while True:
            (playerSocket, address) = self.socket.accept()
            println("Connection " + address[0] + ":" + str(address[1]) + " joined.")
            Avatar(playerSocket, self.casino).start()

if __name__ == '__main__':
    if len(sys.argv) <3:
        print("python server.py HOSTNAME PORT")
    else: 
        Manager(sys.argv[1], sys.argv[2])
    exit(0)
