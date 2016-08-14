import unittest

import ffcut


class TestTime(unittest.TestCase):
    def test_from_string_bad(self):
        self.assertRaises(ValueError, ffcut.Time.from_string,
                          '1:2:3:4')
        self.assertRaises(ValueError, ffcut.Time.from_string,
                          '1:2:3.4.5')
        self.assertRaises(ValueError, ffcut.Time.from_string,
                          'a:b:c')

    def test_from_string(self):
        self.assertEqual(ffcut.Time.from_string('42'),
                         ffcut.Time(0, 0, 42, 0))
        self.assertEqual(ffcut.Time.from_string('42.300'),
                         ffcut.Time(0, 0, 42, 300))
        self.assertEqual(ffcut.Time.from_string('1:42'),
                         ffcut.Time(0, 1, 42, 0))
        self.assertEqual(ffcut.Time.from_string('2:1:42'),
                         ffcut.Time(2, 1, 42, 0))
        self.assertEqual(ffcut.Time.from_string('02:01:42'),
                         ffcut.Time(2, 1, 42, 0))
        self.assertEqual(ffcut.Time.from_string('02:01:42.123'),
                         ffcut.Time(2, 1, 42, 123))

    def test_sum(self):
        first = ffcut.Time(1, 0, 42, 400)
        second = ffcut.Time(0, 2, 2, 0)
        self.assertEqual(first + second,
                         ffcut.Time(1, 2, 44, 400))
