# threading
## 在 擴充 中使用 threading
> [!WARNING]
> 在 CDPS >=1.0.18 後 有更好的方法 使用threading 請看[裝飾器](#new_thread)

### task_run
> [!WARNING]
> 不推薦使用 `onServerCloseEvent` 自行處理
- 需捕獲 Plugin Loader 傳入的 stop_event
```py
import threading
import time

def loop_1(stop_event):
    while not stop_event.is_set():
        print("test")
        time.sleep(3)


def loop_2(stop_event):
    while not stop_event.is_set():
        print("abcd")
        time.sleep(1)


def task_run(stop_event):
    task_thread_1 = threading.Thread(target=loop_1, args=(stop_event,))
    task_thread_1.start()
    task_thread_2 = threading.Thread(target=loop_2, args=(stop_event,))
    task_thread_2.start()
```

### new_thread
```py
from cdps.plugin.thread import new_thread
import time

@new_thread
def loop_1():
    while True:
        print("test")
        time.sleep(3)


@new_thread
def loop_2():
    while True:
        print("abcd")
        time.sleep(1)


loop_1()
loop_2()
```