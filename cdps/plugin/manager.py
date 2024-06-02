import importlib
import json
import os
import shutil
import sys
import zipfile

from cdps.utils.logger import Log
from cdps.utils.version import Version

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
    _instance = None

    def __new__(cls, log: Log = None, event_manager=None):
        if not cls._instance:
            if log is None or event_manager is None:
                raise ValueError(
                    "Initial creation of Plugin instance requires 'log' and 'event_manager' parameters")
            cls._instance = super(Plugin, cls).__new__(cls)
            cls._instance.init(log, event_manager)
        return cls._instance

    def init(self, log: Log, event_manager):
        self.log = log
        self.event_manager = event_manager
        self.loaded_plugins_list = []

        self.modules = {}

        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if os.path.isfile(full_path) and ".cdps" in full_path:
                full_path_folder = full_path.replace(".cdps", "")
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
                    if os.path.isfile(os.path.join(full_path, "cdps.json")):
                        all_plugins.append(entry)
                    else:
                        self.log.logger.error(
                            "Plugin [ {} ] Load Failed (cdps.json)".format(entry))
                else:
                    self.log.logger.error(
                        "Plugin [ {} ] Load Failed (main.py)".format(entry))
        return all_plugins

    def load_info(self, plugins_info, plugins_list):
        for plugin in plugins_list:
            full_path = os.path.join(directory_path, plugin)
            if os.path.isfile(os.path.join(full_path, "cdps.json")):
                with open(os.path.join(full_path, "cdps.json"), 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    plugins_info[plugin] = data

    def dependencies(self, plugins_info: list, plugins_list: list):
        to_remove = []
        for plugin in plugins_list:
            for key, value in plugins_info[plugin]['dependencies'].items():
                if plugins_info.get(key) is None:
                    self.log.logger.error(
                        "Plugin [ {} ] Need Install Dependencies ( {} {} )".format(plugin, key, value))
                    if plugin not in to_remove:
                        to_remove.append(plugin)
                else:
                    ver_use = Version(plugins_info[key]['version'])
                    ver_need = Version(value.replace(">=", ""))
                    if ver_use < ver_need:
                        self.log.logger.error(
                            "Plugin [ {} ] Need Upgrade Dependencies ( {} {} )".format(plugin, key, value))
                        if plugin not in to_remove:
                            to_remove.append(plugin)
        for plugin in to_remove:
            plugins_list.remove(plugin)

    def load_plugins(self, plugins_list):
        for plugin in plugins_list:
            config_path = os.path.join("./config/", "{}.json".format(plugin))
            full_path = os.path.join(directory_path, plugin)
            if os.path.isfile(os.path.join(full_path, "config.json")):
                if not os.path.isfile(config_path):
                    self.log.logger.warning(
                        "Plugin [ {} ] Config Generate".format(plugin))
                    shutil.copy(os.path.join(
                        full_path, "config.json"), config_path)
            self.__reload_module__(plugin, os.path.join(full_path, "main.py"))
            self.log.logger.info("Plugin [ {} ] Loaded".format(plugin))
            self.loaded_plugins_list.append(plugin)
        return self.loaded_plugins_list
    
    def reload_load_plugins(self, name):
        if name in self.loaded_plugins_list:
            config_path = os.path.join("./config/", "{}.json".format(name))
            full_path = os.path.join(directory_path, name)
            if os.path.isfile(os.path.join(full_path, "config.json")):
                if not os.path.isfile(config_path):
                    self.log.logger.warning(
                        "Plugin [ {} ] Config Generate".format(name))
                    shutil.copy(os.path.join(
                        full_path, "config.json"), config_path)
            self.__reload_module__(name, os.path.join(full_path, "main.py"))
            self.log.logger.info("Plugin [ {} ] Reloaded".format(name))
        else:
            self.log.logger.error("Plugin [ {} ] Reload Failed".format(name))

    def __reload_module__(self, module_name, path_to_module):
        spec = importlib.util.spec_from_file_location(
            module_name, path_to_module)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
