import zmq
from zmq.utils.monitor import recv_monitor_message


class controller:

    def __init__(self, register):
        pass

    def start(self, server_url):
        context = zmq.Context()
        socket = zmq.Socket(context, zmq.SUB)
        monitor = socket.get_monitor_socket()

        socket.connect(server_url)
        while True:
            status = recv_monitor_message(monitor)
            if status['event'] == zmq.EVENT_CONNECTED:
                break
            elif status['event'] == zmq.EVENT_CONNECT_DELAYED:
                pass

        print('connected')
        socket.subscribe('tx_trytes')
        while True:
            topic = socket.recv_string()
            topic = topic.split(" ")
            print(topic)
            # data = iota.decode_tryte_method_2(topic[1].encode('utf-8'))
            # More Information https://pyota.readthedocs.io/en/latest/types.html
            # print(data)
