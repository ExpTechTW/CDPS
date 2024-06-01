import os

from setuptools import find_packages, setup

from cdps.constants import core_constant

NAME = core_constant.PACKAGE_NAME
VERSION = core_constant.VERSION
DESCRIPTION = 'Composite Disaster Prevention Server'
AUTHOR = 'ExpTechTW'
REQUIRES_PYTHON = '>=3.8'

CLASSIFIERS = [
    # https://pypi.org/classifiers/
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
]

ENTRY_POINTS = {
	'console_scripts': [
		'{} = {}.entrypoint:entrypoint'.format(core_constant.CLI_COMMAND, core_constant.PACKAGE_NAME)
	]
}
print('ENTRY_POINTS = {}'.format(ENTRY_POINTS))

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as f:
	REQUIRED = list(filter(None, map(str.strip, f)))
	print('REQUIRED = {}'.format(REQUIRED))
	
with open(os.path.join(here, 'README.md'), encoding='utf8') as f:
	LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email='exptech.tw@gmail.com',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    include_package_data=True,
	python_requires=REQUIRES_PYTHON,
	install_requires=REQUIRED,
	classifiers=CLASSIFIERS,
	entry_points=ENTRY_POINTS,
)