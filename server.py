#!/usr/bin/python3

import socket
import threading
import argparse

args = argparse.ArgumentParser()
args.add_argument('-host', help="A host to bind on", required=True, type=str)
args.add_argument('-vp', help="A port to listen on for voice chat", required=True, type=int)
args.add_argument('-cp', help="A port to listen on Command messages", required=True, type=int)
parser = args.parse_args()


class MainServer:
    @staticmethod
    def CreateServer(port, server_type):
        while 1:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((parser.host, port))
                print(f"A {server_type} is running on {port}")
                return s
            except BaseException as e:
                print("Couldn't bind to that port\n", e)
                break


class Server(MainServer):
    def __init__(self):
        self.ip = parser.host
        self.voice_chat = self.CreateServer(parser.vp, "Voice Chat")
        self.command_server = self.CreateServer(parser.cp, "Controller Server")

        self.connections = []
        threading.Thread(target=self.accept_connections)
        threading.Thread(target=self.listenForController)
    def controllerHandler(self):
        pass

    def listenForController(self):
        self.command_server.listen(100)
        print('Running Controller on port: ' + str(parser.cp))
        while True:
            c, addr = self.command_server.accept()
            print("[A new Client Connected {}]".format(addr))
            self.connections.append(c)
            threading.Thread(target=self.controllerHandler, args=(c, addr,)).start()

    def accept_connections(self):
        self.voice_chat.listen(100)
        print('Running Voice Chat on port: ' + str(parser.vp))

        while True:
            c, addr = self.voice_chat.accept()
            print("[A new Client Connected {}]".format(addr))
            self.connections.append(c)

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.voice_chat and client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self, c, addr):
        while 1:
            try:
                data = c.recv(1024)
                # self.broadcast(c, data)
                if hasattr(data, 'decode'):
                    try:
                        string = data.decode("utf-8")
                        print(string)
                        c.send(b'got your message lol')
                    except UnicodeDecodeError:
                        self.broadcast(c, data)


            except socket.error:
                c.close()


server = Server()
