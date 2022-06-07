class network_handler:
    def __init__(self, socket):
        self.socket = socket
        pass

    def receiveMessage(self, is_text):
        length_of_message_length = self.socket.recv(2)

        #print(f"1 - {length_of_message_length}")
        if length_of_message_length == b"":
            return ""
        length_of_message_length_str = length_of_message_length.decode()
        #print(f"2 - {length_of_message_length_str}")
        length_of_message_length = int(length_of_message_length_str)
        #print(f"3 - {length_of_message_length}")
        message_length = int(self.socket.recv(length_of_message_length).decode())

        message = self.socket.recv(message_length)
        while len(message) < message_length:
            message += self.socket.recv(message_length - len(message))

        if is_text == True:
            message = message.decode()

        return message

    def sendMessage(self, message, is_text):
        message_length = len(message)
        #print(f"message_length = {message_length}")
        message_length_str = str(message_length)

        length_of_message_length = len(message_length_str)
        #print(f"length_of_message_length = {length_of_message_length}")

        length_of_message_length_str = str(length_of_message_length).zfill(2)

        self.socket.send(length_of_message_length_str.encode())
        self.socket.send(message_length_str.encode())
        #print(f"message = {message}")
        if is_text == False:
            self.socket.send(message)
        else:
            self.socket.send(message.encode())