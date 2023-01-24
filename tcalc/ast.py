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
