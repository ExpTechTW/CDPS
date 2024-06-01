import sys

from cdps.config import Config
from cdps.constants import core_constant
from cdps.state import State
from cdps.utils.logger import Log


class CDPS:
    def __init__(self, *, generate_default_only: bool = False, initialize_environment: bool = False, focus: bool = False):
        self.log = Log()
        self.log.logger.info("Start {} {}".format(
            core_constant.NAME, core_constant.VERSION))

        self.state = State.INITIALIZING
        self.config = Config()

        if generate_default_only:
            self.config.save_default()
            return

        if initialize_environment:
            if not self.config.file_presents() or focus:
                self.config.save_default()

        try:
            self.log.logger.info("Config File Reading...")
            self.config.read_config(allowed_missing_file=False)
            self.log.logger.info("Config File Readed")

            self.log.logger.setLevel(self.config._data['log_level'])
            self.log.logger.day = self.config._data['log_save_days']
            self.log.clean_old_logs()

            if self.config._data['discord_webhook']['enable']:
                self.log.setup_discord(
                    url=self.config._data['discord_webhook']['url'], level=self.config._data['discord_webhook']['log_level'])
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
        pass