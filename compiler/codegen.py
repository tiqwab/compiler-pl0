import sys
import itertools
from enum import Enum, unique
from compiler.table import RelAddr, Pl0Table

MAX_STACK = 2000
MAX_LEVEL = 5

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
    def __init__(self, table):
        assert isinstance(table, Pl0Table)
        self.table = table
        self.codes = []
        self.c_index = -1

    def next_code(self):
        return self.c_index + 1

    def enter(self, code):
        self.c_index += 1
        if len(self.codes) == self.c_index:
            self.codes.append(code)
        elif len(self.codes) > self.c_index:
            self.codes[self.c_index] = code
        else:
            raise RuntimeError("illegal index: " + self.c_index)

    def gencode_v(self, op_code, value):
        self.enter(ValInst(op_code, value))
        return self.c_index

    def gencode_t(self, op_code, ti):
        self.enter(RefInst(op_code, self.table.reladdr(ti)))
        return self.c_index

    def gencode_o(self, op):
        self.enter(OpInst(op))
        return self.c_index

    def gencode_r(self):
        # skip if the previous code is `ret`
        if self.codes[self.c_index].op_code == OpCode.ret:
            return self.c_index
        self.enter(RetInst(self.table.b_level(), self.table.f_pars()))
        return self.c_index

    def backpatch(self, backp):
        code = self.codes[backp]
        assert isinstance(code, ValInst)
        code.value = self.next_code()

    def execute(self):
        stack = [x for x in itertools.repeat(0, MAX_STACK)]
        display = [x for x in itertools.repeat(0, MAX_LEVEL)]
        pc = top = lev = temp = 0

        while True:
            code = self.codes[pc]
            pc += 1

            if code.op_code == OpCode.lit:
                assert isinstance(code, ValInst)
                stack[top] = code.value
                top += 1
            elif code.op_code == OpCode.lod:
                assert isinstance(code, RefInst)
                stack[top] = stack[display[code.raddr.level] + code.raddr.addr]
                top += 1
            elif code.op_code == OpCode.sto:
                assert isinstance(code, RefInst)
                top -= 1
                stack[display[code.raddr.level] + code.raddr.addr] = stack[top]
            elif code.op_code == OpCode.cal:
                assert isinstance(code, RefInst)
                lev = code.raddr.level + 1
                stack[top] = display[lev]
                stack[top+1] = pc # save pc temporarily
                display[lev] = top
                pc = code.raddr.addr
            elif code.op_code == OpCode.ret:
                assert isinstance(code, RetInst)
                top -= 1
                temp = stack[top]
                top = display[code.raddr.level]
                display[code.raddr.level] = stack[top]
                pc = stack[top+1] # recover pc
                top -= code.raddr.addr
                stack[top] = temp
                top += 1
            elif code.op_code == OpCode.ict:
                assert isinstance(code, ValInst)
                top += code.value
            elif code.op_code == OpCode.jmp:
                assert isinstance(code, ValInst)
                pc = code.value
            elif code.op_code == OpCode.jpc:
                assert isinstance(code, ValInst)
                top -= 1
                if stack[top] == 0:
                    pc = code.value
            elif code.op_code == OpCode.opr:
                assert isinstance(code, OpInst)
                top = self.operate(code, top, stack)

            if pc == 0:
                break

    def operate(self, code, top, stack):
        if code.op == Operator.neg:
            stack[top-1] = -1 * stack[top-1]
            return top
        elif code.op == Operator.add:
            stack[top-2] += stack[top-1]
            return (top-1)
        elif code.op == Operator.sub:
            stack[top-2] -= stack[top-1]
            return (top-1)
        elif code.op == Operator.mul:
            stack[top-2] *= stack[top-1]
            return (top-1)
        elif code.op == Operator.div:
            stack[top-2] /= stack[top-1]
            return (top-1)
        elif code.op == Operator.odd:
            stack[top-1] = stack[top-1] % 2
            return top
        elif code.op == Operator.eq:
            if stack[top-2] == stack[top-1]:
                stack[top-2] = 1
            else:
                stack[top-2] = 0
            return (top-1)
        elif code.op == Operator.ls:
            if stack[top-2] < stack[top-1]:
                stack[top-2] = 1
            else:
                stack[top-2] = 0
            return (top-1)
        elif code.op == Operator.gr:
            if stack[top-2] > stack[top-1]:
                stack[top-2] = 1
            else:
                stack[top-2] = 0
            return (top-1)
        elif code.op == Operator.neq:
            if stack[top-2] != stack[top-1]:
                stack[top-2] = 1
            else:
                stack[top-2] = 0
            return (top-1)
        elif code.op == Operator.lseq:
            if stack[top-2] <= stack[top-1]:
                stack[top-2] = 1
            else:
                stack[top-2] = 0
            return (top-1)
        elif code.op == Operator.greq:
            if stack[top-2] >= stack[top-1]:
                stack[top-2] = 1
            else:
                stack[top-2] = 0
            return (top-1)
        elif code.op == Operator.wrt:
            sys.stdout.write(str(stack[top-1]))
            sys.stdout.flush()
            return (top-1)
        elif code.op == Operator.wrl:
            sys.stdout.write('\n')
            sys.stdout.flush()
            return top
        else:
            raise RuntimeError("illegal op: " + str(code.op))
