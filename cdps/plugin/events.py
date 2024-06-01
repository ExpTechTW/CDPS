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
