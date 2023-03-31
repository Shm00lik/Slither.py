import socket

class TCPClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send(self, data):
        self.socket.send(data.encode())

    def receive(self):
        data = self.socket.recv(1024)
        return data.decode()

    def close(self):
        self.socket.close()