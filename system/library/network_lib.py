# https://realpython.com/python-sockets/
# https://www.programcreek.com/python/example/4400/socket.SO_BROADCAST
# https://github.com/mitsuhiko/phpserialize/issues/15

from socket import socket, AF_INET, SOCK_DGRAM
import socket

class controller:

    def __init__(self, register):
        pass

    def show_message(self, title, message):
        print(message)
        pass

    def create_socket(self, HOST = '', PORT = 65432 ):
        socket_ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        socket_.bind((HOST, PORT))
        return socket_

    def send_message(self, text, HOST = '<broadcast>', PORT = 65432):
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        my_socket.sendto(text, (HOST, PORT))
        my_socket.close()
