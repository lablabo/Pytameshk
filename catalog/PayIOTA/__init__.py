from __future__ import absolute_import, division, print_function, unicode_literals
import zmq
from zmq.utils.monitor import recv_monitor_message
from iota import TryteString


class controller:
    def __init__(self, action, libraries, INIFile):
        iota = libraries['iota']
        iota.test("111")
        # self.testZMG()

    def testZMG(self):
        context = zmq.Context()
        socket = zmq.Socket(context, zmq.SUB)
        monitor = socket.get_monitor_socket()

        #tcp://iota.av.it.pt:5555
        socket.connect("tcp://iota.av.it.pt:5555")
        while True:
            status = recv_monitor_message(monitor)
            print(status)
            if status['event'] == zmq.EVENT_CONNECTED:
                break
            elif status['event'] == zmq.EVENT_CONNECT_DELAYED:
                pass

        print('connected')
        socket.subscribe('tx_trytes')
        while True:
            topic = socket.recv_string()
            print(topic)