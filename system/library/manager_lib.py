import socket


class controller:

    def __init__(self, register):
        pass

    def check(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.config.network.manager_ip , self.config.network.manager_port)
        try:
            sock.connect(server_address)
            print("Manager    :  Connect")
        except Exception as e:
            exit("Manager     :  Disconnect -> %s" %e)
        finally:
            sock.close()
        pass