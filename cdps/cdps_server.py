import sys

from cdps.config import Config
from cdps.constants import core_constant
from cdps.state import State
from cdps.utils.logger import Log
from cdps.plugin.manager import Plugin

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

    def run(self):
        plugin=Plugin()
        plugin.get_all_plugins("./plugins")