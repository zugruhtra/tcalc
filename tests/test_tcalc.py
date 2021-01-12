import unittest

from tcalc.expression import Time
from tcalc.calc import (calc_infix, calc_postfix)
from tcalc.token import (Token, tokenize)


class TestTcalc(unittest.TestCase):

    def test_time(self):
        for expect, given in (
            (Time('01:23:45'), '1:23:45'),
            (Time('00:11:06'), '::666'),
            (Time('00:11:06'), ':11:6'),
        ):
            with self.subTest(expect=expect, args=given):
                self.assertEqual(expect, Time(given))

    def test_tokenize(self):
        for expect, given in (
            ([Token('OPERATOR', '+', 0)], '+'),
            ([Token('SEPERATOR', '(', 0)], '('),
            ([Token('NUMBER', 1.0, 0)], '1.0'),
            ([Token('TIME', Time('1::'), 0)], '1::'),
            ([Token('OPERATOR', '+', 0), Token('OPERATOR', '+', 2)], '+ +'),
        ):
            with self.subTest(expect=expect, args=given):
                self.assertListEqual(expect, list(tokenize(given)))

    def test_calc_postfix(self):
        for expect, given in (
            # generic arithmetic
            (Time('2::'),  '1:: 1:: +'),
            (Time('::'),   '1:: 1:: -'),
            (Time('2::'),  '1:: 2 *'),
            (Time(':30:'), '1:: 2 /'),
            # overflow
            (Time('24::'), '23:59:59 ::1 +'),
        ):
            with self.subTest(expect=expect, args=given):
                self.assertEqual(expect, calc_postfix(tokenize(given)))

    def test_calc_infix(self):
        for expect, given in (
            (Time('3::'), '1:: + 1:: + 1::'),
            (Time('8::'), '(1:: + 1:: ) * 4'),
            (Time('1::'), '( 1:: + 1::) / 2'),
            (4,           '(2 - 1) * 4'),
            (0.5,         '1:: / 2::'),
        ):
            with self.subTest(expect=expect, args=given):
                self.assertEqual(expect, calc_infix(tokenize(given)))

    def test_calc(self):
        for postfix, infix in (
            ('1::0', '1:0:'),
            ('01', '1'),
            ('2.0 2 + 2 -', '2.00'),
            ('1:: 3 * 3 /', '(1/(1.0))*1::'),
            ('1:: 2 /', '1::-1::/2'),
        ):
            with self.subTest(expect=infix, args=postfix):
                self.assertEqual(
                    calc_postfix(tokenize(postfix)),calc_infix(tokenize(infix))
                )
