import importlib
import json
import os
import shutil
import sys
import threading
import zipfile

from cdps.utils.logger import Log
from cdps.utils.version import Version

directory_path = "./plugins/"


class Listener:
    def on_event(self, event):
        raise NotImplementedError("You must implement the on_event method.")


def event_listener(event_type):
    def decorator(listener_class):
        if not hasattr(listener_class, 'on_event'):
            raise ValueError(
                f"Class {listener_class.__name__} must have an 'on_event' method.")
        setattr(listener_class, 'event', event_type)
        manager = Manager._instance
        if manager is None:
            manager = Manager()
        manager.register_listener(listener_class())

        return listener_class
    return decorator


class Manager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Manager, cls).__new__(cls)
            cls._instance.listeners = {}
        return cls._instance

    def register_listener(self, listener):
        event_type = getattr(listener, 'event', None)
        if event_type is None:
            raise ValueError(
                "Listener must have an 'event' attribute defined.")

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

    def __new__(cls, log=None, event_manager=None):
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
        self.modules = {}
        self.plugins_info = {}
        self.all_stopped = threading.Event()
        self.lock = threading.Lock()
        self.loaded_plugins_list = []
        self._load_initial_plugins()

    def _load_initial_plugins(self):
        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if os.path.isfile(full_path) and ".cdps" in full_path:
                full_path_folder = full_path.replace(".cdps", "")
                if os.path.exists(full_path_folder):
                    shutil.rmtree(full_path_folder)
                with zipfile.ZipFile(full_path, 'r') as zip_ref:
                    zip_ref.extractall(full_path_folder)
                os.remove(full_path)

    def get_all_plugins(self):
        all_plugins = []
        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if not "__" in full_path and not os.path.isfile(full_path):
                if os.path.isfile(os.path.join(full_path, "main.py")) and os.path.isfile(os.path.join(full_path, "cdps.json")):
                    all_plugins.append(entry)
                else:
                    self.log.logger.error(
                        f"Plugin [ {entry} ] Load Failed (missing main.py or cdps.json)")
        return all_plugins

    def load_info(self, plugins_info, plugins_list):
        self.plugins_info = plugins_info
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
                if key == plugin:
                    continue
                if plugins_info.get(key) is None:
                    self.log.logger.error(
                        "Plugin [ {} ] Need Install Dependencies ( {} {} )".format(plugin, key, value))
                    if plugin not in to_remove:
                        to_remove.append(plugin)
                    del self.plugins_info[plugin]
                else:
                    ver_use = Version(plugins_info[key]['version'])
                    ver_need = Version(value.replace(">=", ""))
                    if ver_use < ver_need:
                        self.log.logger.error(
                            "Plugin [ {} ] Need Upgrade Dependencies ( {} {} )".format(plugin, key, value))
                        if plugin not in to_remove:
                            to_remove.append(plugin)
                        del self.plugins_info[plugin]
        for plugin in to_remove:
            plugins_list.remove(plugin)

    def load_plugins(self, plugins_list):
        try:
            plugin_load_list = self.get_load_list()
            plugin_load_list.remove("cdps")
            for plugin in plugin_load_list:
                config_path = os.path.join("./config/", f"{plugin}.json")
                full_path = os.path.join(directory_path, plugin)
                if os.path.isfile(os.path.join(full_path, "config.json")) and not os.path.isfile(config_path):
                    shutil.copy(os.path.join(
                        full_path, "config.json"), config_path)
                    self.log.logger.warning(
                        f"Plugin [ {plugin} ] Config Generated")
                completion_event = threading.Event()
                self.__reload_module__(plugin, os.path.join(
                    directory_path, plugin, "main.py"), completion_event)
                completion_event.wait()
                self.log.logger.info(
                    f"Plugin [ {plugin} ] Loaded ( {self.plugins_info[plugin]['version']} )")
                self.loaded_plugins_list.append(plugin)
            return self.loaded_plugins_list
        except Exception as e:
            self.log.logger.error(f"Error Loading Plugins: {e}")

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
            self.log.logger.info("Plugin [ {} ] Reloaded ( {} )".format(
                name, self.plugins_info[name]['version']))
        else:
            self.log.logger.error("Plugin [ {} ] Not Found".format(name))

    def __reload_module__(self, module_name, path_to_module, completion_event=None):
        if module_name in self.modules:
            self.stop_module(module_name)

        stop_event = threading.Event()

        def load_and_run_module():
            spec = importlib.util.spec_from_file_location(
                module_name, path_to_module)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            if hasattr(module, 'task'):
                module.task(stop_event)
            if self.plugins_info[module_name].get('focus-load', False) and hasattr(module, 'initialize'):
                module.initialize(completion_event)
            else:
                completion_event.set()

        thread = threading.Thread(target=load_and_run_module)
        thread.daemon = True
        thread.start()
        self.modules[module_name] = (thread, stop_event)

    def stop_module(self, module_name):
        if module_name in self.modules:
            thread, stop_event = self.modules[module_name]
            stop_event.set()
            thread.join(timeout=5)
            self.log.logger.warning(
                "Plugin [ {} ] Unloaded".format(module_name))

    def stop_all_modules(self):
        for _, (thread, stop_event) in self.modules.items():
            stop_event.set()
            thread.join(timeout=5)

    def get_load_list(self):
        preloaded_plugins = []
        normal_load_order = []
        unresolved_dependencies = {}

        def add_plugin(plugin_name, is_preload):
            if plugin_name in preloaded_plugins or plugin_name in normal_load_order:
                return
            if plugin_name in unresolved_dependencies:
                raise Exception(f"Circular dependency detected: {plugin_name}")
            unresolved_dependencies[plugin_name] = True

            plugin_info = self.plugins_info.get(plugin_name, {})
            dependencies = plugin_info.get('dependencies', [])
            for dependency in dependencies:
                add_plugin(dependency, is_preload)  # 继承父插件的预加载状态

            if is_preload:
                preloaded_plugins.append(plugin_name)
            else:
                normal_load_order.append(plugin_name)

            unresolved_dependencies.pop(plugin_name)

        for plugin, info in self.plugins_info.items():
            add_plugin(plugin, info.get('pre-load', False))

        return preloaded_plugins + normal_load_order
