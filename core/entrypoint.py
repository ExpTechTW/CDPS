import platform
import sys

from core.constants import core_constant
from core.boostrap import boostrap


def __environment_check():
    """

    """
    python_version = sys.version_info.major+sys.version_info.minor*0.1
    if python_version < 3.8:
        print('Python 3.8+ is needed to run {}'.format(core_constant.NAME))
        print('Current Python version {} is too old'.format(
            platform.python_version()))
        sys.exit(1)


def entrypoint():
    boostrap()
    __environment_check()

    from core.cli import cli_entry
    cli_entry.cli_dispatch()
