import argparse
import inspect

from . import __version__
from .report import report


def main():
    parser = argparse.ArgumentParser(description="Commands relating to versioning")
    parser.add_argument('--version', action='version', version='%(prog)s '+__version__)
    
    subparsers = parser.add_subparsers(title='available commands')

    report_parser = subparsers.add_parser('report', help=inspect.getdoc(report))
    report_parser.set_defaults(func=report)
    report_parser.add_argument('packages',metavar='package',type=str,nargs='+',
                               help='name of package')

    args = parser.parse_args()

    if hasattr(args,'func'):
        args.func(*args.packages)
    else:
        parser.error("must supply command to run")
