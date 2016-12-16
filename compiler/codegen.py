from enum import Enum, unique

@unique
class OpCode(Enum):
    lit = 1
    opr = 2
    lod = 3
    sto = 4
    cal = 5
    ret = 6
    ict = 7
    jmp = 8
    jpc = 9

@unique
class Operator(Enum):
    neg = 1
    add = 2
    sub = 3
    mul = 4
    div = 5
    odd = 6
    eq = 7
    ls = 8
    gr = 9
    neq = 10
    lseq = 11
    greq = 12
    wrt = 13
    wrl = 14

class Pl0CodeGenerator:
    def __init__(self):
        pass

    def gencode_v(self, op, v):
        pass

    def gencode_t(op, ti):
        pass

    def gencode_r(self):
        pass

    def gencode_o(self, p):
        pass

    def backpatch(self, backp):
        pass

    def next_code(self):
        pass
