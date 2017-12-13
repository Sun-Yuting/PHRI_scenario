#!/user/bin/env python
# -*- coding: utf-8 -*-

import wx
import socket


class Test(object):

    def __init__(self):
        #self.a = 0
        pass

    def __setattr__(self, key, value):
        super(Test, self).__setattr__(key, value)
        if key == 'a':
            print(self.a)


if __name__ == '__main__':
    server = socket.socket()
    server.bind(('', 20097))
    server.listen(5)
    server, addr = server.accept()

    while True:
        buffer = server.recv(2048).split(b'\n')[0].split(b',')
        if len(buffer) >= 10:
            print(int(buffer[4]))