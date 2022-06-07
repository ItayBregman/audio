import protocol
from networkHandler import network_handler

import socket
import pyglet



def main():
    client = Client(8891, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    client.connection()
    while client.loop():
        continue


class Client:
    def __init__(self, port, socket):
        self.port = port
        self.socket = socket
        self.net_handler = network_handler(self.socket)
        self.player = pyglet.media.Player()


    def connection(self):
        self.socket.connect(("127.0.0.1", self.port))
        print("You are connected!")

        connectMSG = "I'm here and ready"
        self.net_handler.sendMessage(connectMSG, True)

    def loop(self):
        while True:
            command = self.net_handler.receiveMessage(True)
            print("speaker got to " + command)
            if (command == ""):
                print("Server disconnected. By")
                return False
            protocol.clientResponse(command, self.net_handler, self.player)


if __name__ == '__main__':
        main()