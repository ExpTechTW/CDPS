import importlib
import os
import shutil
import sys
import zipfile

directory_path = "./plugins/"


class Listener:
    def on_event(self, event):
        raise NotImplementedError("You must implement the on_event method.")


class Manager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
            cls._instance.listeners = {}
        return cls._instance

    def register_listener(self, listener):
        if listener.event is None:
            raise ValueError(
                "Listener must have an 'event_type' attribute defined.")
        event_type = listener.event
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def call_event(self, event):
        event_type = type(event)
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener.on_event(event)


class Plugin():
    def __init__(self, event_manager) -> None:
        self.event_manager = event_manager

        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if os.path.isfile(full_path):
                if ".cdps" in full_path:
                    full_path_folder = full_path.replace(".zip", "")
                    if os.path.exists(full_path_folder):
                        shutil.rmtree(full_path_folder)
                    with zipfile.ZipFile(full_path, 'r') as zip_ref:
                        zip_ref.extractall(full_path_folder)

    def get_all_plugins(self):
        all_plugins = []
        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if not "__" in full_path and not os.path.isfile(full_path):
                if os.path.isfile(os.path.join(full_path, "main.py")):
                    all_plugins.append(entry)

        return all_plugins

    def load_plugins(self, plugins_list):
        for plugin in plugins_list:
            full_path = os.path.join(directory_path, plugin)
            self.reload_module(plugin, os.path.join(full_path, "main.py"))

    def reload_module(self, module_name, path_to_module):
        spec = importlib.util.spec_from_file_location(
            module_name, path_to_module)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
