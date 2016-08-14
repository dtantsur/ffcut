from __future__ import print_function

import argparse
import logging
import os
import sys

import ffcut


LOG = logging.getLogger(__name__)


class SliceAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not hasattr(namespace, 'slices'):
            namespace.slices = {}

        try:
            last_file = namespace.input[-1]
        except IndexError:
            parser.error('No input files before first take')
            return

        slices = namespace.slices.setdefault(last_file, [])
        take = values.split('..')
        if len(take) != 2:
            parser.error('Takes should be in form "[start]..[end]", '
                         'got %s' % values)
            return

        slices.append(ffcut.Slice(*take))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', action='append',
                        help='Input file(s)')
    parser.add_argument('-s', '--slice', action=SliceAction,
                        help='A slice to include in form of [begin]..[end]')
    parser.add_argument('--copy', action='store_true',
                        help='Whether to use copy instead of re-encoding')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug output')
    parser.add_argument('-o', '--output', required=True, help='Resulting file')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    if args.debug:
        ffcut.FFMPEG_DEBUG = True

    LOG.debug('Arguments %s', args)
    # TODO(dt): check if output file exists

    base_file_name, ext = os.path.splitext(args.output)
    if not ext:
        LOG.warning('Unknown extension for file %s, ffmpeg may fail',
                    args.output)

    outputs = []
    to_delete = []
    try:
        slices = args.slices
    except AttributeError:
        slices = {}

    try:
        for i, input_fname in enumerate(args.input):
            if input_fname in slices:
                out_fname = '%s.part%d%s' % (base_file_name, i, ext)
                ffcut.cut(input_fname, out_fname, slices[input_fname],
                          copy=args.copy)
                outputs.append(out_fname)
                to_delete.append(out_fname)
            else:
                outputs.append(input_fname)

        ffcut.merge(outputs, args.output)
    finally:
        ffcut.safe_delete(to_delete)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print('%s: %s' % (type(exc).__name__, exc), file=sys.stderr)
        sys.exit(1)
