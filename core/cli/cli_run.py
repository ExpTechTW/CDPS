import sys

from core.constants import core_constant
from core.CDPS import CDPS


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