def logical_and(left, right):
    if not left:
        return left
    return bool(right)

def logical_or(left, right):
    if left:
        return left
    return bool(right)