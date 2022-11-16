import sys
import argparse

from tcalc.token import tokenize
from tcalc.calc import (calc_infix, calc_postfix)
from tcalc.exception import ParseError


def get_args():
    parser = argparse.ArgumentParser()
    parser.prog = 'tcalc'
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.description = 'Calculate with Time Expressions'

    parser.add_argument(
        'expr',
        type=str,
        help='a time expression. Use - to read from stdin'
    )

    parser.add_argument(
        '--postfix', '-p',
        action='store_true',
        help='evaluate postfix expression'
    )

    return parser.parse_args()


# Main


def main():
    args = get_args()
    expr = args.expr if args.expr != '-' else sys.stdin.read()

    if args.postfix:
        calc = calc_postfix
    else:
        calc = calc_infix

    try:
        result = calc(tokenize(expr))
    except ParseError as err:
        sys.stderr.write('{}\n'.format(err))
        return 1
    except ZeroDivisionError:
        sys.stderr.write('Divison by Zero!\n')
        return 2

    sys.stdout.write('{}'.format(result))

    return 0


if __name__ == '__main__':
    sys.exit(main())

