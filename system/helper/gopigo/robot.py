from gopigo import *
import sys

class robot:
    def __init__(self, registry):
        self.registry = registry
        pass

    def goRight(self):
        right()
        pass

    def goLeft(self):
        left()
        pass

    def goStop(self):
        stop()
        pass

    def backward(self):
        bwd()
        pass

    def forward(self):
        fwd()
        pass

    def increase(self):
        increase_speed()
        pass

    def decrease(self):
        decrease_speed()
        pass

    def statue(self):
        pass

    def line(self):
        pass

    def distance(self):
        pass
