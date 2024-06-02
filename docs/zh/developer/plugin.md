## [事件](https://github.com/ExpTechTW/CDPS/blob/master/cdps/plugin/events.py)
- 可在 cdps/plugin/events.py 中 查看可用的 events 事件

## 註冊事件
### register_listener (不推薦)
> [!WARNING]
> 在 CDPS >=1.0.15 後 有更好的方法 註冊事件 請看[裝飾器](#event_listener)
```
from cdps.plugin.manager import Listener, Manager # 導入 事件管理器 及 Listener(抽象)
from cdps.plugin.events import onServerStartEvent # 導入 伺服器啟動 事件


class onServerStartListener(Listener): # 定義一個 伺服器啟動事件 監聽器
    event = onServerStartEvent # 定義監聽的事件

    def on_event(self, event): # 實作方法
        print("Hello World")


event_manager = Manager() # 獲取 事件管理器 實例
event_manager.register_listener(onServerStartListener()) # 註冊 監聽器 到 事件管理器
```
### event_listener
```
from cdps.plugin.events import onServerStartEvent
from cdps.plugin.manager import Listener, event_listener


@event_listener(onServerStartEvent) # 裝飾器
class onServerStartListener(Listener):

    def on_event(self, event):
        print(event.pid)
```