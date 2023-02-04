def clampAbs(value, limit):
    right = limit
    left = - limit
    if value < left:
        value = left
    if value > right:
        value = right
    return value

def softClamp(value, limit):
    right = (limit+value*3)/4
    left = - (limit+value*3)/4
    if value < left:
        value = left
    if value > right:
        value = right
    return value

def clamp(left, value, right):
    if value < left:
        value = left
    if value > right:
        value = right
    return value