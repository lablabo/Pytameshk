class config_module:
    def __init__(self, default):
        self.path = default.path + "/catalog/"
        self.loader = "__init__.py"
        self.setup = "setup.ini"
        self.requirements = ['platform', 'numpy', 'socket', 'itertools', 're', 'flask', 'uuid', 'requests',
                             'configparser', 'cryptography']
        self.active = "PayIOTA"
        pass


    def get(self):
        return self