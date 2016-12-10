'''
Functions for basic calculation
'''

plus  = lambda x, y: x + y
minus = lambda x, y: x - y
mul   = lambda x, y: x * y
div   = lambda x, y: x / y

def name_to_op(op):
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
class TopDownParser:
    def __init__(self, expression):
        assert expression is not None

        self.elems = expression.split(' ')
        assert len(self.elems) > 0
        self.elem = None

    def next_elem(self):
        if len(self.elems) == 0:
            return None
        self.elem = self.elems.pop(0)
        return self.elem

    def parse(self):
        self.next_elem()
        return self.expr1()

    def expr1(self):
        t1 = self.term1()
        return self.expr2(t1)

    def expr2(self, t1):
        if len(self.elems) == 0:
            return t1

        if self.elem == '+':
            self.next_elem()
            t2 = self.term1()
            toe = TwoOpExpr(plus, t1, t2)
            return self.expr2(toe)
        else:
            return t1

    def term1(self):
        f1 = self.factor()
        return self.term2(f1)

    def term2(self, f1):
        if len(self.elems) == 0:
            return f1

        if self.elem == '*':
            self.next_elem()
            f2 = self.factor()
            toe = TwoOpExpr(mul, f1, f2)
            return self.term2(toe)
        else:
            return f1

    def factor(self):
        if self.elem == '(':
            self.next_elem()
            e1 = self.expr1()
            self.next_elem()
            return e1
        elif self.is_digit(self.elem):
            n = NumExpr(int(self.elem))
            self.next_elem()
            return n
        else:
            raise RuntimeError("unexpected character: " + self.elem)

    def is_digit(self, v):
        return v in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

'''
main program
'''

def calc_helper(inp):
    tdp = TopDownParser(inp)
    ast = tdp.parse()
    print(ast)
    print(inp, '=', ast.evaluate())

if __name__ == '__main__':
    calc_helper('1')
    calc_helper('1 + 2')
    calc_helper('1 + 2 + 3')
    calc_helper('1 * 2 + 3')
    calc_helper('1 + 2 * 3')
    calc_helper('( 1 + 2 ) * 3')
    calc_helper('( 2 + 5 * 3 ) * ( 1 + 4 * 2 ) + 8')
