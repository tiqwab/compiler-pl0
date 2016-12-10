'''
Functions for basic calculation
'''

plus  = lambda x, y: x + y
minus = lambda x, y: x - y
mul   = lambda x, y: x * y
div   = lambda x, y: x / y

def operator(op):
    '''
    Generate lambda judged by a `op` symbol
    '''
    if op == '+':
        return plus
    elif op == '-':
        return minus
    elif op == '*':
        return mul
    elif op == '/':
        return div
    else:
        raise RuntimeError('illegal operator: ' + op)

def op_to_name(func):
    if func == plus:
        return '+'
    elif func == minus:
        return '-'
    elif func == mul:
        return '*'
    elif func == div:
        return '/'
    else:
        raise RuntimeError("illegal function")

'''
Classes to construct the abstract syntax tree of basic math expression such as '(3 + 5) * 10'
'''

class Expr:
    def __init__(self):
        pass

    def evaluate(self):
        raise NotImplementedError()

class NumExpr(Expr):
    def __init__(self, val):
        super().__init__()
        self.val = val

    def evaluate(self):
        return self.val

    def __str__(self):
        return "NumExpr {val=%s}" % (str(self.val))

    def __repr__(self):
        return "NumExpr {val=%s}" % (repr(self.val))

class TwoOpExpr(Expr):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right

    def evaluate(self):
        return self.op(self.left.evaluate(), self.right.evaluate())

    def __str__(self):
        return "TwoOpExpr {op=%s, left=%s, right=%s}" % (str(op_to_name(self.op)), str(self.left), str(self.right))

    def __repr__(self):
        return "TwoOpExpr {op=%s, left=%s, right=%s}" % (repr(op_to_name(self.op)), repr(self.left), repr(self.right))

'''
Construct the abstract syntax tree
'''

def convert_to_asl(arg_elems):
    assert arg_elems is not None
    assert len(arg_elems) > 0

    elems = list(arg_elems)
    expr_stack = []

    expr(elems, expr_stack)
    return expr_stack.pop()

def expr(elems, stack):
    while len(elems) > 0:
        elem = elems.pop(0)

        if is_num(elem):
            num_expr(elem, stack)
        elif is_op_expr(elem):
            op_expr(elem, elems, stack)
        elif is_op_term(elem):
            op_term(elem, elems, stack)
        elif elem == '(':
            expr(elems, stack)
        elif elem == ')':
            break
        else:
            raise RuntimeError("unexpected eof")

def factor(elems, stack):
    elem = elems.pop(0)
    if is_num(elem):
        num_expr(elem, stack)
    elif elem == '(':
        expr(elems, stack)

def num_expr(elem, stack):
    v = NumExpr(int(elem))
    stack.append(v)

def op_term(elem, elems, stack):
    factor(elems, stack)
    a = stack.pop()
    b = stack.pop()
    v = TwoOpExpr(operator(elem), b, a)
    stack.append(v)

def op_expr(elem, elems, stack):
    expr(elems, stack)
    a = stack.pop()
    b = stack.pop()
    v = TwoOpExpr(operator(elem), b, a)
    stack.append(v)

def is_num(v):
    # FIXME: accept value larger than 9
    return v in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def is_op_expr(v):
    return v in ['+', '-']

def is_op_term(v):
    return v in ['*', '/']

'''
main program
'''

if __name__ == '__main__':
    c = TwoOpExpr(mul, TwoOpExpr(plus, NumExpr(5), NumExpr(3)), NumExpr(10))
    print(c.evaluate())

    input1 = '1 + 2 + 3 - 4'
    asl = convert_to_asl(input1.split(' '))
    print(input1, '=', asl.evaluate())

    input2 = '1 + ( 2 + 3 ) - 4'
    asl = convert_to_asl(input2.split(' '))
    print(input2, '=', asl.evaluate())

    input3 = '2 * 5 + 3'
    asl = convert_to_asl(input3.split(' '))
    print(input3, '=', asl.evaluate())

    input3 = '2 + 5 * 3'
    asl = convert_to_asl(input3.split(' '))
    print(input3, '=', asl.evaluate())

    input3 = '( 2 + 5 * 3 ) * ( 1 + 4 - 2 ) + 8'
    asl = convert_to_asl(input3.split(' '))
    print(asl)
    print(input3, '=', asl.evaluate())
