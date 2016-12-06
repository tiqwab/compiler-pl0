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

class TwoOpExpr(Expr):
    def __init__(self, op, a, b):
        super().__init__()
        self.op = op
        self.a = a
        self.b = b

    def evaluate(self):
        return self.op(self.a.evaluate(), self.b.evaluate())

'''
Construct the abstract syntax tree
'''

def convert_to_asl(arg_elems):
    assert arg_elems is not None
    assert len(arg_elems) > 0

    elems = list(arg_elems)
    expr_stack = []
    while len(elems) > 0:
        elem = elems.pop(0)
        if is_num(elem):
            v = NumExpr(int(elem))
            expr_stack.append(v)
        elif is_op_expr(elem):
            v = op_expr(elem, elems, expr_stack)
            expr_stack.append(v)
    return expr_stack.pop()

def op_expr(elem, elems, stack):
    partial_asl(elems, stack)
    a = stack.pop()
    b = stack.pop()
    return TwoOpExpr(operator(elem), b, a)

def partial_asl(elems, stack):
    elem = elems.pop(0)
    v = NumExpr(int(elem))
    stack.append(v)

def is_num(v):
    # FIXME: accept value larger than 9
    return v in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def is_op_expr(v):
    return v in ['+', '-']

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

'''
main program
'''

if __name__ == '__main__':
    c = TwoOpExpr(mul, TwoOpExpr(plus, NumExpr(5), NumExpr(3)), NumExpr(10))
    print(c.evaluate())

    input1 = '1 + 2 + 3 - 4'
    asl = convert_to_asl(input1.split(' '))
    print(input1, '=', asl.evaluate())
