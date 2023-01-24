import sys
import argparse

from tcalc.reader import InputReader
from tcalc.lexer import Lexer
from tcalc.parser import Parser
from tcalc.evaluator import Evaluator
from tcalc.errors import LexerError, ParserError


def get_args():
    parser = argparse.ArgumentParser()
    parser.prog = "tcalc"
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.description = "Calculate with Time Expressions"

    parser.add_argument(
        "expr", type=str, nargs="?", help="a time expression. Use - to read from stdin"
    )

    return parser.parse_args()


# Main


def evaluate(expr: str) -> int:
    try:
        input_reader = InputReader(expr)
        lexer = Lexer(input_reader)
        parser = Parser(lexer)
        evaluator = Evaluator(parser)
        result = evaluator.eval()
    except ParserError as err:
        sys.stderr.write(expr + "\n")
        sys.stderr.write(" " * (err.column - 1) + "^\n")
        sys.stderr.write(err.msg + "\n")
        return 1
    except LexerError as err:
        sys.stderr.write(err.msg + "\n")
        return 3
    except ZeroDivisionError:
        sys.stderr.write("Divison by Zero!\n")
        return 2

    sys.stdout.write("{}\n".format(result))

    return 0


def main():
    args = get_args()
    expr = args.expr if args.expr != "-" else sys.stdin.read()
    if not expr:
        while True:
            sys.stdout.write("tcalc> ")
            sys.stdout.flush()
            expr = sys.stdin.readline().strip()
            if expr.lower() in ("exit", "quit", "halt"):
                return 0
            rc = evaluate(expr)
            if rc != 0:
                return rc
    else:
        return evaluate(expr)


if __name__ == "__main__":
    sys.exit(main())
