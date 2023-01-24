from enum import Enum, auto
from typing import NamedTuple


class TokenType(Enum):
    # Numbers
    ZERO = auto()
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()
    # Parenthesis
    LPAREN = auto()
    RPAREN = auto()
    # Seperators
    DOT = auto()
    # EOF
    EOF = auto()


class LUT:
    Char2Token = {
        "0": TokenType.ZERO,
        "1": TokenType.ONE,
        "2": TokenType.TWO,
        "3": TokenType.THREE,
        "4": TokenType.FOUR,
        "5": TokenType.FIVE,
        "6": TokenType.SIX,
        "7": TokenType.SEVEN,
        "8": TokenType.EIGHT,
        "9": TokenType.NINE,
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.MULT,
        "/": TokenType.DIV,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        ".": TokenType.DOT,
    }

    Token2Char = {v: k for k, v in Char2Token.items()}


class Token(NamedTuple):
    type: TokenType
    value: str
    column: int


def is_numb(token: Token) -> bool:
    return token.type in (
        TokenType.ZERO,
        TokenType.ONE,
        TokenType.TWO,
        TokenType.THREE,
        TokenType.FOUR,
        TokenType.FIVE,
        TokenType.SIX,
        TokenType.SEVEN,
        TokenType.EIGHT,
        TokenType.NINE,
    )
