import os

from cdps.cdps_server import CDPS


def generate_default_stuffs(*, quiet: bool = False):
	CDPS(generate_default_only=True)
	if not quiet:
		print('Generated default configuration files in {}'.format(os.getcwd()))