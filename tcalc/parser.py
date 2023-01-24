from typing import Protocol, cast

from tcalc.ast import AST, BinaryOperator, UnaryOperator, Number
from tcalc.errors import ParserError
from tcalc.token import Token, LUT, TokenType, is_numb


class Lexer(Protocol):
    def peek(self) -> Token:
        pass

    def consume(self) -> Token:
        pass

    def isEOF(self) -> bool:
        pass


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer

    def parse(self) -> AST:
        ast = self._parse_expression()
        if self._lexer.isEOF():
            return ast
        # some error must occured
        msg = "invalid syntax"
        raise ParserError(msg, self._lexer.peek().column)

    def _parse_expression(self) -> AST:
        node = self._parse_term()

        while self._lexer.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self._lexer.consume()
            node = cast(AST, BinaryOperator(left=node, op=op, right=self._parse_term()))

        return node

    def _parse_term(self) -> AST:
        node = self._parse_factor()

        while self._lexer.peek().type in (TokenType.MULT, TokenType.DIV):
            op = self._lexer.consume()
            node = BinaryOperator(left=node, op=op, right=self._parse_factor())

        return node

    def _parse_factor(self) -> AST:
        if self._lexer.peek().type is TokenType.LPAREN:
            self._lexer.consume()
            node = self._parse_expression()
            token = self._lexer.consume()
            if token.type is not TokenType.RPAREN:
                raise ParserError("unmatched left parenthesis", token.column)
        elif is_numb(self._lexer.peek()) or self._lexer.peek().type is TokenType.DOT:
            node = self._parse_numeric_literal()
        elif self._lexer.peek().type in (TokenType.MINUS, TokenType.PLUS):
            sign = self._lexer.consume()
            node = cast(AST, UnaryOperator(op=sign, expr=self._parse_factor()))
        else:
            raise ParserError("invalid syntax", self._lexer.peek().column)

        return node

    def _parse_numeric_literal(self) -> Number:
        num = self._parse_number()
        return num

    def _parse_number(self) -> Number:
        digits: list[str] = []
        while is_numb(self._lexer.peek()):
            digits.append(self._parse_digit())
        if self._lexer.peek().type is TokenType.DOT:
            self._lexer.consume()
            digits.append(".")
            while is_numb(self._lexer.peek()):
                digits.append(self._parse_digit())
        value = "".join(digits)
        return Number(value)

    def _parse_digit(self) -> str:
        if self._lexer.peek().type is TokenType.ZERO:
            self._lexer.consume()
            return "0"
        return self._parse_non_zero_digit()

    def _parse_non_zero_digit(self) -> str:
        token = self._lexer.consume()
        return LUT.Token2Char[token.type]
