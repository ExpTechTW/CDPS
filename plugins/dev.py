global event_manager

def plugin_event_handler(event_data):
    print(f"插件收到事件，数据：{event_data}")

event.on('on_event', plugin_event_handler)