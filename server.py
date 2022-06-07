import socket
import select

from networkHandler import network_handler
import protocol


def main():
    s = Server()
    while s.handle():
        continue


class Server:

    def __init__(self):
        print("Setting up server...")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("127.0.0.1", 8891))
        self.server_socket.listen()

        print("Listening for clients...")

        self.client_sockets = []
        self.speakers = []
        self.destroy = False


    def handle(self):
        while self.destroy == False:
            try:
                rlist, wlist, xlist = select.select([self.server_socket] + self.client_sockets, self.client_sockets, [])
                for current_socket in rlist:
                    if current_socket is self.server_socket:
                        print(f"new client...")
                        connection, client_address = current_socket.accept()
                        print("New client joined!", client_address)
                        self.client_sockets.append(connection)
                    else:
                        handling = network_handler(current_socket)

                        self.cmd = handling.receiveMessage(True)
                        print("command = " + self.cmd)

                        if(self.cmd == "I'm here and ready"):
                            self.speakers.append(current_socket)
                            continue

                        if(self.cmd == "I'm the gui"):
                            continue

                        if(self.cmd == ""):
                            print("One clients has disconnected. Removing it")
                            self.client_sockets.remove(current_socket)


                        if (self.cmd == "destroy"):
                            print("The Gui disappeared. I'll be exiting now")
                            self.destroy = True

                        if(self.cmd in str(self.speakers)):
                            command = handling.receiveMessage(True)
                            protocol.serverResponse(handling, command, self.speakers, self.cmd)

                        else:
                            protocol.serverResponse(handling, self.cmd, self.speakers, None)

            except KeyboardInterrupt:
                print("Server closing")
                break
        print("closing")
        return False

if __name__ == "__main__":
    main()