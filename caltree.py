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

    # while len(elems) > 0:
    #     expr(elems, expr_stack)
    expr(elems, expr_stack)
    return expr_stack.pop()

def expr(elems, stack):
    while len(elems) > 0:
        elem = elems.pop(0)

        if is_num(elem):
            num_expr(elem, stack)
        elif is_op_expr(elem):
            op_expr(elem, elems, stack)
        elif elem == '(':
            expr(elems, stack)
        elif elem == ')':
            break
        else:
            raise RuntimeError("unexpected eof")

def num_expr(elem, stack):
    v = NumExpr(int(elem))
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

    input2 = '1 + ( 2 + 3 ) - 4'
    asl = convert_to_asl(input2.split(' '))
    print(input2, '=', asl.evaluate())
