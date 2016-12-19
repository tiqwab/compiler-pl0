from unittest import TestCase, main
from compiler.table import RelAddr
from compiler.codegen import OpCode, Operator, ValInst, RefInst,\
                             OpInst, RetInst, Pl0CodeGenerator

class TestPl0CodeGenerator(TestCase):
    def setUp(self):
        pass

    def test_gen(self):
        a = ValInst(OpCode.ict, 4)
        b = RefInst(OpCode.lod, RelAddr(1, 1))
        c = OpInst(Operator.add)
        d = RetInst(1, 1)
        print(a, b, c, d)

    def tearDown(self):
        pass

if __name__ == '__main__':
    main()
