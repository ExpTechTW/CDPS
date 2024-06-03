import functools
import threading
from typing import Callable, Optional, Union

from cdps.utils import misc_util

__all__ = [
    'new_thread',
    'FunctionThread'
]


class FunctionThread(threading.Thread):
    __NONE = object()

    def __init__(self, target, name, args, kwargs):
        super().__init__(target=target, args=args, kwargs=kwargs, name=name, daemon=True)
        self.__return_value = self.__NONE
        self.__error = None

        def wrapped_target(*args_, **kwargs_):
            try:
                self.__return_value = target(*args_, **kwargs_)
            except Exception as e:
                self.__error = e
                raise e from None

        self._target = wrapped_target

    def get_return_value(self, block: bool = False, timeout: Optional[float] = None):
        if block:
            self.join(timeout)
        if self.__return_value is self.__NONE:
            if self.is_alive():
                raise RuntimeError('The thread is still running')
            raise self.__error
        return self.__return_value


def new_thread(arg: Optional[Union[str, Callable]] = None):
    def wrapper(func):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            thread = FunctionThread(
                target=func, args=args, kwargs=kwargs, name=thread_name)
            thread.start()
            return thread
        misc_util.copy_signature(wrap, func)
        wrap.original = func
        return wrap
    if isinstance(arg, Callable):
        thread_name = None
        return wrapper(arg)
    else:
        thread_name = arg
        return wrapper
