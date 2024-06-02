from cdps.plugin.manager import Plugin
from cdps.utils.logger import Log
from cdps.constants import core_constant


class console_cdps():
    def __init__(self, args):
        self.loop = True
        self.args = args
        self.log = Log()
        if self.args[1]:
            if self.args[1] == "plugin":
                self.__plugin__()
            elif self.args[1] == "version":
                self.log.logger.info('{} {}'.format(
                    core_constant.NAME, core_constant.VERSION))
            elif self.args[1] == "exit":
                self.loop = False
                self.log.logger.warn('{} {} Good Bye!!!'.format(
                    core_constant.NAME, core_constant.VERSION))
            else:
                self.log.logger.error("Unknow Command! ( cdps )")
        else:
            self.log.logger.error("Unknow Command! ( cdps )")

    def __plugin__(self):
        if self.args[2]:
            if self.args[2] == "reload":
                Plugin().reload_load_plugins(self.args[3])
            elif self.args[2] == "load":
                self.log.logger.warning("Not Implemented! ( cdps plugin )")
            elif self.args[2] == "unload":
                self.log.logger.warning("Not Implemented! ( cdps plugin )")
            else:
                self.log.logger.error("Unknow Command! ( cdps plugin )")
        else:
            self.log.logger.error("Unknow Command! ( cdps plugin )")

# cdps plugin reload example
