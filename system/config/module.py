class config_module:
    def __init__(self, default):
        self.path = default.path + "/catalog/"
        self.loader = "__init__.py"
        self.requirements = ['platform', 'numpy', 'socket', 'itertools', 're', 'flask', 'uuid', 'requests', 'cryptography']
        self.active = "blockchain"
        pass


    def get(self):
        return self