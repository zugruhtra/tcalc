from collections import deque
from typing import Protocol

from tcalc.token import TokenType, Token, LUT
from tcalc.errors import LexerError


class InputReader(Protocol):
    def peek(self) -> tuple[str, int]:
        pass

    def next(self) -> tuple[str, int]:
        pass

    def isEOF(self) -> bool:
        pass


class Lexer:
    def __init__(self, input_stream: InputReader) -> None:
        self.input_stream = input_stream
        self._tokens: deque[Token] = deque()
        self._idx = 0

        self._scan_all()

    def peek(self) -> Token:
        if len(self._tokens) > 0:
            return self._tokens[-1]
        else:
            raise LexerError("No next token")

    def consume(self) -> Token:
        if len(self._tokens) > 0:
            return self._tokens.pop()
        else:
            raise LexerError("No more tokens to consume")

    def isEOF(self) -> bool:
        try:
            return self._tokens[-1].type is TokenType.EOF
        except IndexError:
            return False

    def _scan_all(self) -> None:
        while True:
            self._scan_next()
            if self._tokens[0].type is TokenType.EOF:
                break

    def _scan_next(self) -> None:
        if self.input_stream.isEOF():
            self._tokens.appendleft(Token(TokenType.EOF, "", self._idx))
            return

        value, column = self.input_stream.next()
        self._idx += 1
        if value in (" ", "\t", "\n"):
            return

        try:
            token_type = LUT.Char2Token[value]
        except KeyError:
            raise LexerError(f"Unknown character: {value}", column)

        token = Token(token_type, value, column)
        self._tokens.appendleft(token)
