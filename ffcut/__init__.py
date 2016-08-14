import collections


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
