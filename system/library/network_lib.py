from socket import *


class controller:

    def __init__(self, register):
        pass

    def create_socket(self):
        cs = socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        cs.sendto('This is a test', ('255.255.255.255', 54545))
        pass
