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

class Pl0CodeGenerator:
    def __init__(self):
        pass

    def gencode_v(self, op, v):
        pass

    def gencode_r(self):
        pass

    def backpatch(self, backp):
        pass

    def next_code(self):
        pass
