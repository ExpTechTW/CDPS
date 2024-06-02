## Inject 注入
- Server 啟動時會 觸發 `onServerStartEvent`
- 如果我的 擴充 想在 `onServerStartEvent` 前做些什麼 ( 通常是自製的 `日誌擴充` 等 需要在其他擴充前 初始化完成 )
- 這時 `Inject 注入` 就登場了
- 注入新的 `onServerStartEventForExample` 讓其在 `onServerStartEvent` 前 先被執行

### 原始 類、方法
- cdps/plugin/events.py
```py
class onServerStartEvent(Event):
    """ 當 伺服器 啟動 """

    def __init__(self, pid):
        self.pid = pid
```
- cdps/cdps_server.py
```py
def on_start(self):
    self.event_manager.call_event(onServerStartEvent("start"))
```
### 定義新的類
```py
from cdps.plugin.events import Event

class onServerStartEventForExample(Event):
    """ 當 伺服器 啟動 """
    def __init__(self, pid):
        self.pid = pid
```
### 保留原始方法
```py
original_on_start = cdps.cdps_server.CDPS.on_start
```
### 定義新方法
```py
def _new_on_start(self):
    self.event_manager.call_event(onServerStartEventForExample("example")) # 多了這行
    original_on_start(self) # 呼叫原始方法
```
### 注入
```py
cdps.cdps_server.CDPS.on_start = _new_on_start
```

## 完成看起來像這樣
```py
from cdps.plugin.events import Event
import cdps.cdps_server

class onServerStartEventForExample(Event):
    """ 當 伺服器 啟動 """
    def __init__(self, pid):
        self.pid = pid

original_on_start = cdps.cdps_server.CDPS.on_start

def _new_on_start(self):
    self.event_manager.call_event(onServerStartEventForExample("example"))
    original_on_start(self)

cdps.cdps_server.CDPS.on_start = _new_on_start

class onServerStartEventForExampleListener(Listener):
    event = onServerStartEventForExampleEvent

    def on_event(self, event):
        print(event.pid)
; :
event_manager = Manager()
event_manager.register_listener(onServerStartEventForExampleListener()) # 別忘了監聽事件
```