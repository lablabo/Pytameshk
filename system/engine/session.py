class sessions:
    def __init__(self):
        self.session_ = 0
        pass

    def start(self):
        self.session_ = Session()
        return self.session_
