import os
import sys

from cdps.config import Config
from cdps.console.cdps import console_cdps
from cdps.constants import core_constant
from cdps.plugin.events import (onCommandEvent, onServerCloseEvent,
                                onServerStartEvent)
from cdps.plugin.manager import Manager, Plugin
from cdps.state import State
from cdps.utils.logger import Log


class CDPS:
    def __init__(self, *, generate_default_only: bool = False, initialize_environment: bool = False):
        self.log = Log()
        self.log.logger.info("Start {} {}".format(
            core_constant.NAME, core_constant.VERSION))

        self.state = State.INITIALIZING
        self.config = Config()

        if generate_default_only:
            self.config.save_default()
            return

        if initialize_environment:
            if not self.config.file_presents():
                self.config.save_default()

        try:
            self.log.logger.info("Config File Reading...")
            self.config.read_config(allowed_missing_file=False)
            self.log.logger.info("Config File Readed")

            self.log.logger.setLevel(self.config._data['log_level'])
            self.log.logger.day = self.config._data['log_save_days']
            self.log.clean_old_logs()
        except Exception as e:
            self.log.logger.error(
                "Please use the [init] command to initialize the project")
            sys.exit(1)

    def is_initialized(self) -> bool:
        if self.state == State.INITIALIZED:
            return True
        else:
            return False

    def on_start(self):
        self.event_manager.call_event(onServerStartEvent(os.getpid()))

    def on_close(self, reason):
        self.event_manager.call_event(onServerCloseEvent(reason))

    def run(self):
        self.loop = True
        try:
            self.event_manager = Manager()
            plugin = Plugin(self.log, self.event_manager)
            self.all_plugins = plugin.get_all_plugins()
            self.plugins_info = {"cdps": core_constant.INFO}
            plugin.load_info(
                self.plugins_info, self.all_plugins)
            plugin.pip_dependencies(self.plugins_info, self.all_plugins)
            plugin.dependencies(self.plugins_info, self.all_plugins)
            plugin.load_plugins(self.all_plugins)
            self.on_start()

            while self.loop:
                command = input()
                if command != "":
                    args = command.split()
                    if args[0] == "cdps" or args[0] == "CDPS":
                        console = console_cdps(args)
                        self.loop = console.loop
                    else:
                        self.event_manager.call_event(onCommandEvent(command))
        except KeyboardInterrupt as e:
            print("Program was stopped by user")
        finally:
            self.on_close(1)
            plugin.stop_all_modules()
            print("Exiting the program...")
