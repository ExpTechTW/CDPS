import importlib
import os
import sys


class Plugin():
    def __init__(self,event_manager) -> None:
        self.event_manager = event_manager

    def get_all_plugins(self, directory_path):
        all_plugins = []
        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if os.path.isfile(full_path):
                # if ".zip" in full_path:
                all_plugins.append(entry.replace(".zip", ""))
                self.reload_module("dev",full_path)
            else:
                all_plugins.append(entry)
                print(full_path)

        print(all_plugins)
        return all_plugins

    def reload_module(self, module_name, path_to_module):
        spec = importlib.util.spec_from_file_location(
            module_name, path_to_module)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        module.event = self.event_manager
        spec.loader.exec_module(module)
        return module
