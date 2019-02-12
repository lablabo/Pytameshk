import string

class action:
    def __init__(self, route, args={}):
        self.path = ""
        route = route.strip("/")
        self.parts = route.split('/')
        print(self.parts)
        pass
    