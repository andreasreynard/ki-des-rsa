import socket
from threading import Thread
import index_key
import pka
from datetime import datetime
import secrets
import json
import client2

class Client:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(('127.0.0.1', 2024))
        self.talk_to_server()

    def talk_to_server(self):
        self.socket.send('client1'.encode())
        Thread(target = self.receive_message).start()
        self.send_message()

    def send_message(self):
        while True:
            client_input = input('')
            cur_key = '0369cf258be147ad'
            enc_message = index_key.encrypt(client_input.encode('utf-8').hex(), index_key.key(cur_key))
            private_key1, public_key2 = self.get_keys(0)
            # Client1 sends a message to Client2
            nonce = secrets.token_hex(16)
            enc_key1 = []
            for char in cur_key:
                enc_key1.append(pka.better_pow(int(char, 16), private_key1))
            encrypts = [enc_message]
            for char in enc_key1:
                encrypts.append(pka.better_pow(char, public_key2))
            encrypts.append(nonce)
            print(f"Client1 sent message encrypted with Client2's public key to Client2: [Client1 || {nonce}]")
            self.socket.send(json.dumps(encrypts).encode())

    def receive_message(self):
        while True:
            result = json.loads(self.socket.recv(1024).decode())
            enc_message, enc_key2, nonce1, nonce2 = result[0], result[1:-2], result[-2], result[-1]
            private_key1, public_key2 = self.get_keys(1)
            enc_key1 = []
            for char in enc_key2:
                enc_key1.append(pka.better_pow(char, private_key1))
            cur_key = ''
            for char in enc_key1:
                cur_key += hex(pka.better_pow(char, public_key2))[2:]
            server_inbox = bytes.fromhex(index_key.decrypt(enc_message, index_key.key(cur_key))).decode('utf-8')
            print(f'Client1 verified Nonce1: {nonce1}, and received message: {server_inbox}, with Nonce2: {nonce2}')
            self.send_nonce(nonce2)

    def send_nonce(self, nonce2):
        cur_key = '05af49e38d27c16b'
        enc_nonce = index_key.encrypt(nonce2, index_key.key(cur_key))
        private_key1, public_key2 = self.get_keys(1)
        enc_key1 = []
        for char in cur_key:
            enc_key1.append(pka.better_pow(int(char, 16), private_key1))
        encrypts = [enc_nonce]
        for char in enc_key1:
            encrypts.append(pka.better_pow(char, public_key2))
        print(f"Client1 sent Nonce2 encrypted with Client2's public key back to Client2: {enc_nonce}")
        client2.final_step(encrypts)

    def get_keys(self, requested):
        # Generate keys
        private_key1 = pka.gen_keys(1)[0]
        public_key2 = pka.gen_keys(2)[1]
        if requested == 0:
            # Client1 requests Client2's public key from the PKA
            request = "Get Client2's public key || Timestamp: " + datetime.now().isoformat()
            print(request)
            # Verify PKA's response
            print(f"Client2's public key verified from PKA: {pka.verified()} [{public_key2} || {request}]")
        return private_key1, public_key2

if __name__ == '__main__':
    Client()
