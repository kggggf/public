#!/usr/bin/python
# modified by SunYeop Lee from https://raw.githubusercontent.com/kbatten/python-socks5-socket/master/monkey_sockets_socks5.py

from struct import pack, unpack
from socket import *

class Socks5Socket(socket):    
    def __init__(self, host, port, proxyhost, proxyport):
        super(Socks5Socket, self).__init__()

        self.connect((proxyhost, proxyport)) # socks5 proxy

        ####################### socks5 proxy connection #######################
        # greet the socks server
        msg = pack("!BB", 0x05, 1) # auth_methods_available = 1
        msg += pack("!B", 0x00) # auth_methods = [0x00]
        self.send(msg)
        resp = self.recv(2)
        (version, auth_method) = unpack("!BB", resp)

        # set connection to tcp/ip stream, ipv4
        ipb = map(int, gethostbyname(host).split(".")) # hostname -> ip
        msg = pack("!B B B B BBBB H",0x05,0x01,0x00,0x01,ipb[0],ipb[1],ipb[2],ipb[3],port)
        self.send(msg)
        resp = self.recv(10)
        (version, status) = unpack("!B B 8x", resp)

        # check status
        if status != 0:
            self.close()
            raise Exception("socks connection failed, error: " + str(status))

# test
import re
s = Socks5Socket('ipip.kr', 80, 'localhost', 9150)
s.send("GET / HTTP/1.1\r\nHost: ipip.kr\r\n\r\n")
print re.search("<title>(.*?)</title>", s.recv(400)).group(1)
