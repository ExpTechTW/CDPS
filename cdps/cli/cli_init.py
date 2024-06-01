import os

from cdps.cdps_server import CDPS
from cdps.constants import core_constant


def initialize_environment(*, quiet: bool = False):
    CDPS(initialize_environment=True)
    if not quiet:
        print('Initialized environment for {} in {}'.format(
            core_constant.NAME, os.getcwd()))
