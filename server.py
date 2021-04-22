#!/usr/bin/python3

import socket
import threading
import argparse

args = argparse.ArgumentParser()
args.add_argument('-host', help="A host to bind on", required=True, type=str)
args.add_argument('-p', help="A port to listen on", required=True, type=int)
parser = args.parse_args()


class Server:
    def __init__(self):
        self.ip = parser.h
        self.port = parser.p
        self.s = self.CreateServer()
        # while 1:
        #     try:
        #
        #
        #         self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #         self.s.bind((self.ip, self.port))
        #
        #         break
        #     except:
        #         print("Couldn't bind to that port")
        #         break

        self.connections = []
        self.accept_connections()

    def CreateServer(self):
        while 1:
            try:

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((self.ip, self.port))

                return s

            except:
                print("Couldn't bind to that port")
                break

    def accept_connections(self):
        self.s.listen(100)

        print('Running on IP: ' + self.ip)
        print('Running on port: ' + str(self.port))

        while True:
            c, addr = self.s.accept()
            print("[A new Client Connected {}]".format(addr))
            self.connections.append(c)

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
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
