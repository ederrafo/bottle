# -*- coding: utf-8 -*-
__author__ = 'myth'


import socket
import struct
def get_ip_address(ifname):
    try:
        import fcntl
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    except:
        return  socket.gethostbyname(socket.gethostname())

        # name_ex = socket.gethostbyname_ex(socket.gethostname())

    #get_ip_address('lo')环回地址
    #get_ip_address('eth0')主机ip地址


