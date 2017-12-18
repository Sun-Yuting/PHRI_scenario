#!/user/bin/env python
# -*- coding: utf-8 -*-

import socket
import time


class Net():
    """network class, singleton, 3 sockets: for TTS & for behavior manager & for phri sensing part"""

    # python's __new__ method returns a uninitialized object
    def __init__(self):
        #self.client_bm, self.client_tts = self.connect_clients()
        self.server, self.server2 = self.connect_server()
        print('net init')

    @staticmethod
    def connect_clients():
        host_bm = "127.0.0.1"
        port_bm = 20099
        host_tts = "127.0.0.1"
        port_tts = 20100
        retries = 5  # try 5 times

        client_bm = socket.socket()
        print('trying to connect behavior manager...')
        for i in range(retries):
            try:
                client_bm.connect((host_bm, port_bm))
            except socket.error:
                time.sleep(2)
            if i == retries - 1:
                raise ConnectionError('cannot connect to behavior manager!')
        print('behavior manager connected.')

        client_tts = socket.socket()
        print('trying to connect tts engine...')
        for i in range(retries):
            try:
                client_tts.connect((host_tts, port_tts))
            except socket.error:
                time.sleep(2)
            if i == retries - 1:
                raise ConnectionError('cannot connect to tts engine!')
        print('tts engine connected.')

        return client_bm, client_tts

    @staticmethod
    def connect_server():
        print('server waiting for connection...')

        server = socket.socket()
        port = 20098
        server.bind(('', port))
        server.listen(5)
        client, addr = server.accept()

        print('server connected.')

        server2 = socket.socket()
        server2.bind(('', 20097))
        server2.listen(5)
        server2, addr = server2.accept()

        return client, server2

    def send(self, command, target):
        if target == 'tts':
            # tts format: Play voice_name content delay
            user = 'watanabe_ver4.0_22'
            tokens = command.split(' ')
            tts_command = f'Play {user} {tokens[1]}'
            self.client_tts.send(tts_command)
        elif target == 'bm':
            self.client_bm.send(command)
        else:
            raise ValueError(f'no such target: {target}!')

    def recv(self, source):
        assert source in ['tts', 'bm', 'sensing']

        if source == 'tts':
            buffer = self.client_tts.recv(2048).split(b'\x00')[0]
            return buffer
        elif source == 'bm':
            buffer = self.client_bm.recv(2048).split(b'\x00')[0]
            return buffer
        elif source == 'sensing':
            # didn't know the length, set to 2048
            # error on decode? /x00/xcc/xcc... /x00 is the end of a line
            # add b'' to split
            buffer = self.server.recv(2048).split(b'\x00')[0]
            buffer2 = self.server2.recv(2048).split(b'\n')[0]
            return f'{buffer2} {buffer}'
        else:
            raise ValueError(f'no such source: {source}!')
