from tcalc.token import Token


class AST:
    pass


class BinaryOperator(AST):
    def __init__(self, left: AST, op: Token, right: AST) -> None:
        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        return f"BinOp({self.op}, {str(self.left)}, {str(self.right)})"


class UnaryOperator(AST):
    def __init__(self, op: Token, expr: AST) -> None:
        self.op = op
        self.expr = expr

    def __str__(self) -> str:
        return f"UnaryOp({self.op}, {str(self.expr)})"


class Number(AST):
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"Numb({self.value})"


class Time(AST):
    def __init__(self, hours: str, minutes: str, seconds: str) -> None:
        self.hours = hours if hours else "0"
        self.minutes = minutes if minutes else "0"
        self.seconds = seconds if seconds else "0"

    def __str__(self) -> str:
        return f"Time({self.hours}, {self.minutes}, {self.seconds})"
