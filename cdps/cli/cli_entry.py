import sys
from argparse import ArgumentParser

from cdps.cli.cli_gendefault import generate_default_stuffs
from cdps.cli.cli_init import initialize_environment
from cdps.cli.cli_run import run
from cdps.cli.cli_version import show_version
from cdps.constants import core_constant


def cli_dispatch():
    if len(sys.argv) == 1:
        run()
        return

    parser = ArgumentParser(
        prog=core_constant.CLI_COMMAND,
        description='{} CLI'.format(core_constant.NAME),
    )
    parser.add_argument(
        '-q', '--quiet', help='Disable CLI output', action='store_true')
    parser.add_argument('-v', '--version', help='Print {} version and exit'.format(
        core_constant.NAME), action='store_true')
    subparsers = parser.add_subparsers(
        title='Command', help='Available commands', dest='subparser_name')

    subparsers.add_parser('start', help='Start {}'.format(core_constant.NAME))
    subparsers.add_parser(
        'init', help='Prepare the working environment of {}. Create commonly used folders and generate default configuration and permission files'.format(core_constant.NAME))
    subparsers.add_parser(
        'init-focus', help='Prepare the working environment of {}. Create commonly used folders and generate default configuration and permission files'.format(core_constant.NAME))
    subparsers.add_parser(
        'gendefault', help='Generate default configuration and permission files at current working directory. Existed files will be overwritten')

    # parser_pack = subparsers.add_parser('pack', help='Pack files into a packed')
    # parser_pack.add_argument('-n', '--name', help='A specific name to the output file. If not given the metadata specific name or a default one will be used', default=None)

    args = parser.parse_args()

    if args.version:
        show_version(quiet=args.quiet)
        return

    if args.subparser_name == 'start':
        run()
    elif args.subparser_name == 'init':
        initialize_environment(quiet=args.quiet)
    elif args.subparser_name == 'init-focus':
        initialize_environment(quiet=args.quiet, focus=True)
    elif args.subparser_name == 'gendefault':
        generate_default_stuffs(quiet=args.quiet)
    # elif args.subparser_name == 'pack':
    # 	make_packed(args, quiet=args.quiet)
