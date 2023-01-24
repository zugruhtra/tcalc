class Error(Exception):
    def __init__(self, msg: str, column: int) -> None:
        self.msg = msg
        self.column = column


class ParserError(Error):
    pass


class LexerError(Error):
    def __init__(self, msg: str, column: int = -1):
        self.msg = msg
        self.column = column
