from unittest import TestCase, main
from unittest.mock import Mock, ANY, call
from compiler.table import RelAddr, Pl0Table
from compiler.codegen import OpCode, Operator, ValInst, RefInst,\
                             OpInst, RetInst, Pl0CodeGenerator

class TestPl0CodeGenerator(TestCase):
    def setUp(self):
        self.table = Mock(Pl0Table)
        self.sut = Pl0CodeGenerator(self.table)

    def test_gencode_with_var_and_const(self):
        '''
        Assume the below source program.

        const m = 5;
        var x;
        begin
          x := m;
          write x;
        end.
        '''
        # Setup
        self.table.reladdr.side_effect = [RelAddr(1,1), RelAddr(2,2), RelAddr(3,3)]
        self.table.b_level.return_value = 1
        self.table.f_pars.return_value = 1
        # Execute
        back_p = self.sut.gencode_v(OpCode.jmp, 0)
        self.sut.backpatch(back_p)
        self.sut.next_code()
        self.sut.gencode_v(OpCode.ict, 7)
        self.sut.gencode_t(OpCode.lod, 2)
        self.sut.gencode_t(OpCode.sto, 3)
        self.sut.gencode_t(OpCode.lod, 4)
        self.sut.gencode_o(Operator.wrt)
        self.sut.gencode_r()
        # Assert
        expect_codes = [ ValInst(OpCode.jmp, 1)
                       , ValInst(OpCode.ict, 7)
                       , RefInst(OpCode.lod, RelAddr(1,1))
                       , RefInst(OpCode.sto, RelAddr(2,2))
                       , RefInst(OpCode.lod, RelAddr(3,3))
                       , OpInst(Operator.wrt)
                       , RetInst(1,1)
                       ]
        self.assertEqual(self.sut.codes, expect_codes)

    def test_gencode_with_func(self):
        '''
        Assume the below source program.

        function foo()
        begin
          return (1 + 2)
        end
        begin
          write foo()
        end.
        '''
        # Setup
        self.table.reladdr.side_effect = [RelAddr(1,1)]
        self.table.b_level.return_value = 1
        self.table.f_pars.return_value = 0
        # Execute
        back_p1 = self.sut.gencode_v(OpCode.jmp, 0)
        self.sut.next_code()
        back_p2 = self.sut.gencode_v(OpCode.jmp, 0)
        self.sut.backpatch(back_p2)
        self.sut.next_code()
        self.sut.gencode_v(OpCode.ict, 7)
        self.sut.gencode_v(OpCode.lit, 1)
        self.sut.gencode_v(OpCode.lit, 2)
        self.sut.gencode_o(Operator.add)
        self.sut.gencode_r()
        self.sut.backpatch(back_p1)
        self.sut.next_code()
        self.sut.gencode_v(OpCode.ict, 7)
        self.sut.gencode_t(OpCode.cal, 8)
        self.sut.gencode_o(Operator.wrt)
        self.sut.gencode_r()
        # Assert
        expect_codes = [ ValInst(OpCode.jmp, 7)
                       , ValInst(OpCode.jmp, 2)
                       , ValInst(OpCode.ict, 7)
                       , ValInst(OpCode.lit, 1)
                       , ValInst(OpCode.lit, 2)
                       , OpInst(Operator.add)
                       , RetInst(1, 0)
                       , ValInst(OpCode.ict, 7)
                       , RefInst(OpCode.cal, RelAddr(1,1))
                       , OpInst(Operator.wrt)
                       , RetInst(1, 0)
                       ]
        self.assertEqual(self.sut.codes, expect_codes)

    def tearDown(self):
        pass

if __name__ == '__main__':
    main()
