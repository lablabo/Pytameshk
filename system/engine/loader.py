import os
import sys
import importlib

class loader:
    def __init__(self, registry):
        self.data_ = registry
        self.config = registry.get("config")
        self.report = registry.get("log")
        self.modules_path = self.config.module.path
        self.active_module = self.config.module.active
        self.active_module_dir = self.modules_path + self.active_module + "/"
        self.module_loader = self.config.module.loader
        self.module_loader_path = self.active_module_dir + self.module_loader
        self.libraries = {}
        pass

    def controller(self):
        self.check_module_exist()
        self.check_module_loader()
        self.load_libraries()
        self.load_modules()
        pass

    def check_module_exist(self):
        modules = [name for name in os.listdir(self.modules_path) if os.path.isdir(self.modules_path + name)]
        if self.active_module not in modules:
            print("Module (" + self.active_module + ") Not Exist")
            self.report.error("file", "Module (" + self.active_module + ") Not Exist", "engine/static/loader", True)
        pass

    def load_libraries(self):
        sys.path.insert(1, self.config.library.path)
        files = [name for name in os.listdir(self.config.library.path)]
        for lib in files:
            if(lib not in self.config.library.ignore):
                lib_name  = lib.replace('.py', '')
                lib_class = importlib.import_module(lib_name)
                globals()["load_lib_class"] = lib_class
                lib_obj = load_lib_class.controller(self.data_)
                self.libraries[lib_name.replace('_lib', '')] =  lib_obj

    def load_modules(self):
        sys.path.insert(1, self.modules_path)
        try:
            my_module = importlib.import_module(self.active_module)
        except:
            print("Import Module Error")
            self.report.error("file", "Import Module -> " + self.active_module + " Error", "system/engine/loader", True)
        globals()["load_module_data"] = my_module
        load_module_data.controller(self.data_, self.libraries)

    def check_module_loader(self):
        files = [name for name in os.listdir(self.active_module_dir) if os.path.isfile(self.active_module_dir + name)]
        if self.module_loader not in files:
            print(self.active_module + " -> " + self.module_loader + " Not Exist")
            self.report.error("file", self.active_module + " -> " + self.module_loader + " Not Exist", "system/engine/loader", True)
        pass
