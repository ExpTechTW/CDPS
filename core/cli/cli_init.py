import os

from core.constants import core_constant
from core.CDPS import CDPS


def initialize_environment(*, quiet: bool = False, focus: bool = False):
    CDPS(initialize_environment=True, focus=focus)
    if not quiet:
        print('Initialized environment for {} in {}'.format(
            core_constant.NAME, os.getcwd()))
