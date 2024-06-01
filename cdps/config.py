"""
MCDR config file stuffs
"""
from typing import Any, Dict, Tuple, Union

from cdps.utils.yaml_data_storage import YamlDataStorage

CONFIG_FILE = 'config.yml'
DEFAULT_CONFIG_RESOURCE_PATH = '/resources/default_config.yml'

class Config(YamlDataStorage):
    def __init__(self):
        super().__init__(CONFIG_FILE, DEFAULT_CONFIG_RESOURCE_PATH)

    def set_values(self, changes: Dict[Union[Tuple[str], str], Any]):
        with self._data_operation_lock:
            for keys, value in changes.items():
                if isinstance(keys, str):
                    keys = tuple(keys.split('.'))
                assert len(keys) > 0
                data = self._data
                for i, key in enumerate(keys):
                    if key not in data:
                        raise KeyError(
                            'Unknown config key {} at index {}'.format(keys, i))
                    if i < len(keys) - 1:
                        data = data[key]
                    else:
                        data[key] = value

    def is_debug_on(self):
        for value in self._data['debug']:
            if value is True:
                return True
        return False
