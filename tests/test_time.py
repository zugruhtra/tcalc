import unittest
from decimal import Decimal

from tcalc.expression import Time


def build_time(s, sign=False):
    ts = s.split(":")
    return Time(
        hours=Decimal(ts[0] if ts[0] else "0"),
        minutes=Decimal(ts[1] if ts[1] else "0"),
        seconds=Decimal(ts[2] if ts[2] else "0"),
        sign=sign,
    )


class TestTime(unittest.TestCase):
    def test_addition_minutes(self):
        t1 = build_time("::59")
        t2 = build_time("::1")
        expected = build_time(":1:")
        result = t1 + t2
        self.assertEqual(result, expected)
    
    def test_addition_hours(self):
        t1 = build_time(":59:")
        t2 = build_time(":1:")
        expected = build_time("1::")
        result = t1 + t2
        self.assertEqual(result, expected)
    
    def test_subtraction_minutes(self):
        t1 = build_time(":1:")
        t2 = build_time("::1")
        expected = build_time("::59")
        result = t1 - t2
        self.assertEqual(result, expected)

    def test_subtraction_underflow(self):
        t1 = build_time('::1')
        t2 = build_time("::2")
        expected = build_time("::1", True)
        result = t1 - t2
        self.assertEqual(result, expected)

    def test_multiplication(self):
        t = build_time("5:3:2")
        scalar = 20
        expected = build_time("101:0:40")
        result = t * scalar
        self.assertEqual(result, expected)
    
    def test_division_with_scalar(self):
        t = build_time("9:6:3")
        scalar = Decimal(3)
        expected = build_time("3:2:1")
        result = t / scalar
        self.assertEqual(result, expected)

    def test_division_with_time(self):
        t1 = build_time("9:6:3")
        t2 = build_time("3:2:1")
        expected = Decimal(3)
        result = t1 / t2
        self.assertEqual(result, expected)
    
    def test_negate(self):
        t1 = build_time("1:1:1")
        t2 = build_time("1:1:1")
        expected = build_time("::")
        result = t1 + -t2
        self.assertEqual(result, expected)