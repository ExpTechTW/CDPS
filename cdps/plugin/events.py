class Event:
    pass


class onServerStartEvent(Event):
    """ 當 伺服器 啟動 """

    def __init__(self, pid):
        self.pid = pid


class onServerCloseEvent(Event):
    """ 當 伺服器 關閉 """

    def __init__(self, reason):
        self.reason = reason


class onCommandEvent(Event):
    """ 當 用戶輸入 到 控制台 """

    def __init__(self, command):
        self.command = command


class onPluginReloadEvent(Event):
    """ 當 擴充 將被 重新讀取 """

    def __init__(self, name):
        self.name = name
