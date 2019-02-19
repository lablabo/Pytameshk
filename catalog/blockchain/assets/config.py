class custom_config:

    HOST = None
    PORT = None

    def __init__(self):

        self.HOST = '127.0.01' # Standard loopback interface address (localhost)
        self.PORT = 65432 # Port to listen on (non-privileged ports are > 1023)

        pass


