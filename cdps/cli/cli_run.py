import sys

from cdps.cdps_server import CDPS
from cdps.constants import core_constant


def run():
	try:
		cdps = CDPS()
	except Exception as e:
		print('Fail to initialize {}: ({}) {}'.format(core_constant.NAME, type(e), e), file=sys.stderr)
		raise

	if not cdps.is_initialized():
		cdps.run()
	else:
		pass