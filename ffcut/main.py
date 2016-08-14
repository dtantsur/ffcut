import argparse
import sys

import ffcut


class TakeAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not hasattr(namespace, 'takes'):
            namespace.takes = {}

        try:
            last_file = namespace.input[-1]
        except IndexError:
            parser.error('No input files before first take')
            return

        takes = namespace.takes.setdefault(last_file, [])
        take = values.split('..')
        if len(take) != 2:
            parser.error('Takes should be in form "[start]..[end]", '
                         'got %s' % values)
            return

        takes.append(ffcut.Slice(*take))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', nargs='+',
                        help='Input file')
    parser.add_argument('-t', '--take', action=TakeAction,
                        help='A cut to take in form of [begin]..[end]')
    parser.add_argument('--copy', action='store_true',
                        help='Whether to use copy instead of re-encoding')
    parser.add_argument('-o', '--output', required=True, help='Resulting file')
    args = parser.parse_args()

    print args


if __name__ == '__main__':
    sys.exit(main())
