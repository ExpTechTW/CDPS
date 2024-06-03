import inspect
import threading
from typing import Callable, Iterable, List, Optional, Tuple, TypeVar


def start_thread(func: Callable, args: Tuple, name: Optional[str] = None):
    thread = threading.Thread(target=func, args=args, name=name, daemon=True)
    thread.start()
    return thread


T = TypeVar('T')


def unique_list(lst: Iterable[T]) -> List[T]:
    return list(dict.fromkeys(lst).keys())


def deep_copy_dict(source: dict) -> dict:
    ret = {}
    for key, value in source.items():
        if isinstance(value, dict):
            value = deep_copy_dict(value)
        ret[key] = value
    return ret


def copy_signature(target: Callable, origin: Callable) -> Callable:
    assert callable(target) and callable(origin)
    target.__signature__ = inspect.signature(origin)
    return target
