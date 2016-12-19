from enum import Enum, unique
from compiler.table import RelAddr, Pl0Table

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

class Inst:
    def __init__(self, op_code):
        self.op_code = op_code

class ValInst(Inst):
    def __init__(self, op_code, value):
        super().__init__(op_code)
        self.value = value

    def __str__(self):
        return "ValInst {op_code=%s, value=%d}" % (str(self.op_code), self.value)

    def __repr__(self):
        return "ValInst {op_code=%s, value=%d}" % (str(self.op_code), self.value)

    def __eq__(self, other):
        if other is None or not isinstance(other, ValInst):
            return False
        return self.op_code == other.op_code and self.value == other.value

class RefInst(Inst):
    def __init__(self, op_code, raddr):
        super().__init__(op_code)
        self.raddr = raddr

    def __str__(self):
        return "RefInst {op_code=%s, raddr=%s}" \
                % (str(self.op_code), str(self.raddr))

    def __repr__(self):
        return "RefInst {op_code=%s, raddr=%s}" \
                % (str(self.op_code), str(self.raddr))

    def __eq__(self, other):
        if other is None or not isinstance(other, RefInst):
            return False
        return self.op_code == other.op_code and self.raddr == other.raddr

class OpInst(Inst):
    def __init__(self, op):
        super().__init__(OpCode.opr)
        self.op = op

    def __str__(self):
        return "OpInst {op_code=%s, op=%s}" % (str(self.op_code), str(self.op))

    def __repr__(self):
        return "OpInst {op_code=%s, op=%s}" % (str(self.op_code), str(self.op))

    def __eq__(self, other):
        if other is None or not isinstance(other, OpInst):
            return False
        return self.op_code == other.op_code and self.op == other.op

class RetInst(Inst):
    def __init__(self, level, pars):
        super().__init__(OpCode.ret)
        self.raddr = RelAddr(level, pars)

    def __str__(self):
        return "RetInst {op_code=%s, raddr=%s}" \
                % (str(self.op_code), str(self.raddr))

    def __repr__(self):
        return "RetInst {op_code=%s, raddr=%s}" \
                % (str(self.op_code), str(self.raddr))

    def __eq__(self, other):
        if other is None or not isinstance(other, RetInst):
            return False
        return self.op_code == other.op_code and self.raddr == other.raddr

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
