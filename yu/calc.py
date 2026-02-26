import re
from .global_definition import e2, e3, e5, illegal_charM, invalid_numberM, paren_mismatchM

def tokenize(expr):
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or ch == '.':
            start = i
            dot_seen = False
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                if expr[i] == '.':
                    if dot_seen:
                        raise ValueError(invalid_numberM)
                    dot_seen = True
                i += 1
            num_str = expr[start:i]
            if '.' in num_str:
                tokens.append(float(num_str))
            else:
                tokens.append(int(num_str))
            continue
        if ch in '+-*/%^()':
            tokens.append(ch)
            i += 1
        else:
            raise ValueError(illegal_charM.format(ch))
    return tokens

def apply_operator(op, a, b=None):
    if op == 'u-':
        return -a
    elif op == 'u+':
        return a
    elif op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            raise ZeroDivisionError(e2)
        return a / b
    elif op == '%':
        if b == 0:
            raise ZeroDivisionError(e2)
        return a % b
    elif op == '^':
        return a ** b
    else:
        raise ValueError(f"Unknown Operator: {op}")

def precedence(op):
    if op in ('u-', 'u+'):
        return 4
    if op in ('+', '-'):
        return 1
    if op in ('*', '/', '%'):
        return 2
    if op == '^':
        return 3
    return 0

def is_right_associative(op):
    return op in ('^', 'u-', 'u+')

def evaluate_expression(expr_str):
    tokens = tokenize(expr_str)
    if not tokens:
        return None, "Empty"
    values = []
    operators = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if isinstance(token, (int, float)):
            values.append(token)
            i += 1
            continue
        if token == '(':
            operators.append(token)
            i += 1
            continue
        if token == ')':
            while operators and operators[-1] != '(':
                op = operators.pop()
                if op in ('u-', 'u+'):
                    if len(values) < 1:
                        raise ValueError(e3)
                    val = values.pop()
                    values.append(apply_operator(op, val))
                else:
                    if len(values) < 2:
                        raise ValueError(e3)
                    b = values.pop()
                    a = values.pop()
                    res = apply_operator(op, a, b)
                    values.append(res)
            if not operators or operators[-1] != '(':
                raise ValueError(paren_mismatchM)
            operators.pop()
            i += 1
            continue
        if token in ('-', '+'):
            if i == 0 or (i > 0 and tokens[i-1] in ('+','-','*','/','%','^','(')):
                token = 'u-' if token == '-' else 'u+'
        while operators and operators[-1] != '(':
            top = operators[-1]
            if (precedence(top) > precedence(token)) or \
               (precedence(top) == precedence(token) and not is_right_associative(token)):
                op = operators.pop()
                if op in ('u-', 'u+'):
                    if len(values) < 1:
                        raise ValueError(e3)
                    val = values.pop()
                    values.append(apply_operator(op, val))
                else:
                    if len(values) < 2:
                        raise ValueError(e3)
                    b = values.pop()
                    a = values.pop()
                    res = apply_operator(op, a, b)
                    values.append(res)
            else:
                break
        operators.append(token)
        i += 1
    while operators:
        op = operators.pop()
        if op == '(':
            raise ValueError(paren_mismatchM)
        if op in ('u-', 'u+'):
            if len(values) < 1:
                raise ValueError(e3)
            val = values.pop()
            values.append(apply_operator(op, val))
        else:
            if len(values) < 2:
                raise ValueError(e3)
            b = values.pop()
            a = values.pop()
            res = apply_operator(op, a, b)
            values.append(res)
    if len(values) != 1:
        return None, e5
    return values[0], None

def calc(expr_str):
    try:
        result, error = evaluate_expression(expr_str)
        if error:
            return f"Error: {error}"
        else:
            return result
    except Exception as e:
        return f"Error: {e}"