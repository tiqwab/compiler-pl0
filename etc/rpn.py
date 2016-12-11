import sys

operators = {
    '+': 6,
    '-': 6,
    '*': 7,
    '/': 7,
}

def calc_rpn(rpn):
    '''
    Evalute a reverse polish notation.

    > calc_rpn(['2', '3', '2', '*', '5', '3', '*', '+', '*'])
    42.0
    '''
    assert rpn is not None
    assert len(rpn) > 0

    stack = []
    while len(rpn) > 0:
        elem = rpn.pop(0)
        if elem in operators.keys():
            expr2 = stack.pop()
            expr1 = stack.pop()
            if elem == '+':
                stack.append(expr1 + expr2)
            elif elem == '-':
                stack.append(expr1 - expr2)
            elif elem == '*':
                stack.append(expr1 * expr2)
            elif elem == '/':
                stack.append(expr1 / expr2)
            else:
                raise RuntimeError('Invalid operator: ' + elem)
        else:
            stack.append(float(elem))
    return stack[0]

def convert_to_rpn(elems):
    '''
    Convert a polish notation to reverse polish notation.

    > convert_to_rpn(['2', '*', '(', '3', '*', '2', '+', '5', '*', '3', ')'])
    ['2', '3', '2', '*', '5', '3', '*', '+', '*']
    '''
    assert elems is not None

    if len(elems) == 0:
        return []

    accum = []
    stack = []
    while len(elems) > 0:
        elem = elems.pop(0)
        if elem == '(':
            accum = accum + convert_to_rpn(elems)
        elif elem == ')':
            break
        elif elem in operators.keys():
            while len(stack) > 0 and operators[stack[-1]] >= operators[elem]:
                op = stack.pop()
                accum.append(op)
            stack.append(elem)
        else:
            accum.append(elem)
    while len(stack) > 0:
        op = stack.pop()
        accum.append(op)
    return accum

if __name__ == '__main__':
    '''
    Accept expression and calculate
    '''
    elems = sys.argv[1].split(' ')
    print(calc_rpn(convert_to_rpn(elems)))
