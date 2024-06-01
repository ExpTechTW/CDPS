import os
from threading import RLock

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from cdps.utils import file_util, resources_util
from cdps.utils.lazy_item import LazyItem


class YamlDataStorage:
    def __init__(self, file_path: str, default_file_path: str):
        self.__file_path = file_path
        self.__default_file_path = default_file_path
        self.__default_data = LazyItem(
            lambda: resources_util.get_yaml(self.__default_file_path))
        self._data = CommentedMap()
        self._data_operation_lock = RLock()

    def __getitem__(self, option: str):
        return self._data[option]

    def file_presents(self) -> bool:
        return os.path.isfile(self.__file_path)

    def read_config(self, allowed_missing_file: bool):
        if self.file_presents():
            with open(self.__file_path, encoding='utf8') as file:
                data = YAML().load(file)
        else:
            if not allowed_missing_file:
                raise FileNotFoundError()
            data = {}
        self._data = data
        return None

    def __save(self, data: CommentedMap):
        with file_util.safe_write(self.__file_path, encoding='utf8') as file:
            yaml = YAML()
            yaml.width = 1048576  # prevent yaml breaks long string into multiple lines
            yaml.dump(data, file)

    def save(self):
        with self._data_operation_lock:
            self.__save(self._data)

    def get_default_yaml(self):
        return self.__default_data.get()

    def save_default(self):
        self.__save(self.get_default_yaml())
