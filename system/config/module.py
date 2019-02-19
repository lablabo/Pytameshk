class config_module:
    def __init__(self, default):
        self.path = default.path + "/catalog/"
        self.loader = "__init__.py"
        self.requirements = ['platform', 'numpy', 'socket', 'itertools', 're', 'flask', 'uuid', 'requests']
        self.active = "ehsan"
        pass


    def get(self):
        return self