import socket
from threading import Thread
from pkauth import public_key
import libfunc
import json

class Client:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(('127.0.0.1', 2024))
        self.talk_to_server()

    def talk_to_server(self):
        self.socket.send("client2".encode())
        Thread(target = self.receive_message).start()
        self.send_message()

    def send_message(self):
        while True:
            client_input = input("")
            own_key = public_key(2)
            n = own_key[1]
            enc_message = libfunc.encoder(client_input, [libfunc.mod_inv(own_key[0], libfunc.phi(n)), n])
            self.socket.send(json.dumps(enc_message).encode())

    def receive_message(self):
        while True:
            enc_message = json.loads(self.socket.recv(1024).decode())
            server_inbox = libfunc.decoder(enc_message, public_key(1))
            print("Inbox: " + ''.join(str(p) for p in server_inbox))

if __name__ == '__main__':
    Client()
