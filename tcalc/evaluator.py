from decimal import Decimal
from typing import Protocol

from tcalc.ast import AST, BinaryOperator, Time, UnaryOperator, Number
from tcalc.token import TokenType
from tcalc.expression import Time as TimeExpr


class Parser(Protocol):
    def parse(self) -> AST:
        pass


class Evaluator:
    def __init__(self, parser: Parser) -> None:
        self.parser = parser

    def eval(self) -> Decimal | TimeExpr:
        ast = self.parser.parse()
        result = self.visit(ast)
        return result

    def visit(self, ast: AST) -> Decimal | TimeExpr:
        if type(ast) is BinaryOperator:
            if ast.op.type is TokenType.PLUS:
                return self.visit(ast.left) + self.visit(ast.right)  # type: ignore
            elif ast.op.type is TokenType.MINUS:
                return self.visit(ast.left) - self.visit(ast.right)  # type: ignore
            elif ast.op.type is TokenType.MULT:
                return self.visit(ast.left) * self.visit(ast.right)  # type: ignore
            elif ast.op.type is TokenType.DIV:
                return self.visit(ast.left) / self.visit(ast.right)  # type: ignore
            else:
                assert False, "unreachable line"
        elif type(ast) is UnaryOperator:
            if ast.op.type is TokenType.PLUS:
                return self.visit(ast.expr)
            elif ast.op.type is TokenType.MINUS:
                return -self.visit(ast.expr)
            else:
                assert False, "unreachable line"
        elif type(ast) is Number:
            return Decimal(ast.value)
        elif type(ast) is Time:
            return TimeExpr(
                Decimal(ast.hours),
                Decimal(ast.minutes),
                Decimal(ast.seconds),
            )
        else:
            assert False, "unreachable line"
