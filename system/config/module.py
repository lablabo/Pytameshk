class config_module:
    def __init__(self, default):
        # Active Module on Catalog Directory
        self.active = "PayIOTA"

        # Requirement Packages
        self.requirements = [
            'platform',
            'numpy',
            'socket',
            'itertools',
            're', 'flask',
            'uuid',
            'requests',
            'configparser',
            'cryptography',
            'hashlib',
            'json',
            'urllib',
            'time',
            'requests',
            'uuid',
            'sqlite3',
            'iota',
            'random',
            'socket',
            'random',
            'math',
            'threading',
            'zmq',
        ]

        self.path = default.path + "/catalog/"
        self.loader = "__init__.py"
        self.setup = "setup.ini"
        pass

    def get(self):
        return self