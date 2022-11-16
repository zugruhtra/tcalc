import re
from collections import namedtuple

from tcalc.exception import ParseError
from tcalc.expression import Time


TOKEN_SPEC = (
        ('TIME',      r'\d*:\d*:\d*'),
        ('NUMBER',    r'\d+(\.\d*)?'),
        ('OPERATOR',  r'[+\-*/]'),
        ('SEPERATOR', r'[\(\)]'),
        ('SKIP',      r'[ \t]+'),
        ('MISMATCH',  r'.'),
        )

RE_TOKEN_SPEC = re.compile(
        '|'.join('(?P<{}>{})'.format(*pair) for pair in TOKEN_SPEC))


Token = namedtuple('Token', ['type', 'value', 'column'])


def tokenize(code):
    line_start = 0
    for match in RE_TOKEN_SPEC.finditer(code):
        kind = match.lastgroup
        value = match.group()
        column = match.start() - line_start
        if kind == 'TIME':
            value = Time(value)
        elif kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise ParseError('{}\n{}\nUnexpected token'.format(
                code, ' ' * (column + line_start) + '^'))
        yield Token(kind, value, column)

