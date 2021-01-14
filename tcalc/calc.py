from .exception import ParseError


PRECEDENCE = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        }


def precedenc(token):
    return PRECEDENCE[token.value]


def is_binop(token):
    return token.type == 'OPERATOR'


def is_seperator(token):
    return token.type == 'SEPERATOR'


def is_time(token):
    return token.type == 'TIME'


def is_number(token):
    return token.type == 'NUMBER'


def bin_compute(left, operator, right):
    if operator == '+':
        return left + right
    elif operator == '-':
        return left - right
    elif operator == '*':
        return left * right
    elif operator == '/':
        return left / right
    else:
        raise NotImplementedError(
                'Operator "{}" not implemented'.format(operator))


def shunting_yard(expr):
    stack = []
    for token in expr:
        if is_number(token) or is_time(token):
            yield token
        elif is_binop(token):
            while len(stack) != 0 and is_binop(stack[-1]) \
                    and precedenc(token) <= precedenc(stack[-1]):
                yield stack.pop()
            stack.append(token)
        elif is_seperator(token):
            if token.value == '(':
                stack.append(token)
            elif token.value == ')':
                while stack[-1].value != '(':
                    yield stack.pop()
                stack.pop()
    while len(stack) != 0:
        yield stack.pop()


def calc_postfix(expr):
    stack = []
    for token in expr:
        if is_time(token) or is_number(token):
            stack.append(token.value)
        elif is_binop(token):
            right = stack.pop()
            left = stack.pop()
            result = bin_compute(left, token.value, right)
            stack.append(result)
        else:
            raise ParseError('Unknown token: {}'.format(token))
    if len(stack) > 1:
        raise ParseError('Unused tokens in the stack: {}'.format(stack))
    elif len(stack) == 0:
        raise ParseError('Empty stack')
    return stack.pop()


def calc_infix(expr):
    return calc_postfix(shunting_yard(expr))

