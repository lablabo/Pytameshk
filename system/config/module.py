class config_module:
    def __init__(self, default):
        self.path = default.path + "/catalog/"
        self.loader = "__init__.py"
        self.requirements = ['platform', '__future__', 'numpy', 'socket', 'itertools', 're']
        self.active = "blockchain"
        pass


    def get(self):
        return self