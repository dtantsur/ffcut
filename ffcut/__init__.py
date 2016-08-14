import collections
import logging
import os
import shutil
import subprocess


LOG = logging.getLogger(__name__)
FFMPEG_DEBUG = False


class Time(collections.namedtuple('Time', ('hour', 'minute', 'second', 'ms'))):
    """Time: a moment on a timeline."""
    @classmethod
    def from_string(cls, s):
        """Parse ffmpeg-compatible string [[h:]m:]s[.ms]."""
        components = s.split(':')
        hour = minute = second = msecond = 0

        if len(components) > 3:
            raise ValueError('Too many components separated by : in %s' % s)
        elif len(components) == 3:
            hour, minute, second = components
        elif len(components) == 2:
            minute, second = components
        else:
            second = components[0]

        if '.' in second:
            second, msecond = second.split('.', 1)

        return cls(int(hour), int(minute), int(second), int(msecond))

    def __add__(self, other):
        # TODO(dt): fix overflow (maybe just switch to stdlib time?)
        return Time(*(x + y for (x, y) in zip(self, other)))

    def to_ffmpeg(self):
        return '%s:%s:%s.%s' % self


class EndOfFile(object):
    def __str__(self):
        return "Time(EOF)"

    __repr__ = __str__


EOF = EndOfFile()


class Slice(collections.namedtuple('Slice', ('begin', 'end'))):
    """Slice: a period of time with a beginning and an end."""
    def __new__(cls, begin, end):
        if not begin:
            begin = Time(0, 0, 0, 0)
        elif not isinstance(begin, Time):
            begin = Time.from_string(begin)

        if not end:
            end = EOF
        elif not isinstance(end, Time):
            delta = False
            if end and end[0] == '+':
                delta = True
                end = end[1:]

            end = Time.from_string(end)
            if delta:
                end = begin + end

        return super(Slice, cls).__new__(cls, begin, end)


def ffmpeg(cmd):
    """Run ffmpeg with a given command line."""
    base_cmd = ['ffmpeg', '-y']
    if not FFMPEG_DEBUG:
        base_cmd += ['-loglevel', 'error']
    cmd = base_cmd + list(cmd)
    LOG.debug('Running %s', cmd)
    return subprocess.check_call(cmd)


def safe_delete(files):
    if not isinstance(files, list):
        files = [files]

    for fname in files:
        try:
            os.remove(fname)
        except EnvironmentError as exc:
            LOG.warning('Unable to delete file %s: %s', fname, exc)


def merge(input_files, output_file_name):
    """Merge several similar files into one."""
    if len(input_files) == 1:
        LOG.info('Copying resulting file %s into %s',
                 input_files[0], output_file_name)
        shutil.copy(input_files[0], output_file_name)
        return

    files_fname = '%s.files.txt' % output_file_name
    with open(files_fname, 'wt') as fp:
        for fname in input_files:
            fp.write("file %s\n" % fname)

    cmd = ['-f', 'concat', '-safe', '0', '-i', files_fname,
           '-c', 'copy', output_file_name]
    LOG.info('Merging chunks %s into file %s', input_files, output_file_name)
    try:
        ffmpeg(cmd)
    finally:
        safe_delete(files_fname)


def cut(input_file_name, output_file_name, slices, copy=False):
    """Cut several slices from a file, then merge them back."""
    base_cmd = ['-i', input_file_name]
    base_file_name, ext = os.path.splitext(output_file_name)

    files = []
    try:
        for i, s in enumerate(slices):
            cmd = base_cmd + ['-ss', s.begin.to_ffmpeg()]
            if s.end is not EOF:
                cmd += ['-to', s.end.to_ffmpeg()]
            if copy:
                cmd += ['-c', 'copy']
            fname = '%s.chunk%d%s' % (base_file_name, i, ext)
            cmd.append(fname)

            LOG.info('Splitting %s of file %s into temporary file %s',
                     s, input_file_name, fname)
            ffmpeg(cmd)
            files.append(fname)

        merge(files, output_file_name)
    finally:
        safe_delete(files)
