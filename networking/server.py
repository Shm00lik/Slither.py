import socket

class UDPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))

    def receive(self):
        data, addr = self.socket.recvfrom(1024)
        return data.decode()

    def send(self, data, addr):
        self.socket.sendto(data.encode(), addr)

    def close(self):
        self.socket.close()
