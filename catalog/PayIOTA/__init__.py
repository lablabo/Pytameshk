import zmq
import threading
import time
import msgpack as serializer
from zmq.utils.monitor import recv_monitor_message

class controller:
    def __init__(self, action, libraries):
        print("Start Pay IOTA")
        self.testZMG()

    def testZMG(self):
        context = zmq.Context()
        socket = zmq.Socket(context, zmq.SUB)
        monitor = socket.get_monitor_socket()

        socket.connect("tcp://iota.av.it.pt:5555")
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
            print(topic)
            #payload = serializer.loads(socket.recv(), encoding='utf-8')
            #print(topic, payload)