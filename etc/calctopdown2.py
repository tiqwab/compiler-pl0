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
Classes to express the abstract syntax tree of basic math expression such as '(3 + 5) * 10'
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
Construct the abstract syntax tree(use 'while')

E  -> T {(+T| -T)}
T  -> F {(*F| /F)}
F  -> (E) | N
N  -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
('e' means empty)
'''
class TopDownParser:
    def __init__(self, expression):
        assert expression is not None

        self.tokens = expression.split(' ')
        assert len(self.tokens) > 0
        self.token = None

    def next_token(self):
        '''
        Parse a next token, but just return one character.
        '''
        if self.empty():
            self.token = None
            return None
        self.token = self.tokens.pop(0)
        return self.token

    def empty(self):
        return len(self.tokens) == 0

    def parse(self):
        '''
        Parse a given input to the abstract syntax tree.
        '''
        self.next_token()
        return self.expr()

    def expr(self):
        acc = self.term()
        while self.token in ['+', '-']:
            op = self.token
            self.next_token()
            second = self.term()
            if op == '+':
                acc = TwoOpExpr(plus, acc, second)
            else:
                acc = TwoOpExpr(minus, acc, second)
        return acc

    def term(self):
        acc = self.factor()
        while self.token in ['*', '/']:
            op = self.token
            self.next_token()
            second = self.factor()
            if op == '*':
                acc = TwoOpExpr(mul, acc, second)
            else:
                acc = TwoOpExpr(div, acc, second)
        return acc

    def factor(self):
        if self.token == '(':
            self.next_token()
            e = self.expr()
            self.next_token() # for ')'
            return e
        elif self.is_digit(self.token):
            n = NumExpr(int(self.token))
            self.next_token()
            return n
        else:
            raise RuntimeError("unexpected character: " + self.token)

    def is_digit(self, v):
        return v in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

'''
Main program.
Parse and calculate basic math expressions.
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
    calc_helper('( 2 - 5 * 3 ) + ( 4 * 3 / 2 - 1 ) * 2')
