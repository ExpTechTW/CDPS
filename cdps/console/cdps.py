from cdps.plugin.manager import Plugin


class console_cdps():
    def __init__(self, args):
        self.args = args
        if self.args[1] == "plugin":
            self.__plugin__()

    def __plugin__(self):
        if self.args[2] == "reload":
            Plugin().reload_load_plugins(self.args[3])

# cdps plugin reload example
