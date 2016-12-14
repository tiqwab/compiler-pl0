from unittest import TestCase, main
from unittest.mock import Mock, ANY, call
from compiler.getsource import SourceReader
from compiler.table import IdKind, Pl0Table
from compiler.codegen import OpCode, Operator, Pl0CodeGenerator
from compiler.compile import Pl0Compiler

class TestCompile(TestCase):
    def setUp(self):
        pass

    def setUpReader(self, file_name):
        self.reader = SourceReader(file_name)
        self.table = Mock(spec=Pl0Table)
        self.gen = Mock(spec=Pl0CodeGenerator)
        self.sut = Pl0Compiler(self.reader, self.table, self.gen)

    def test_compile_decl(self):
        # Setup
        self.setUpReader('test/original3-1.pl')
        # Execute
        self.sut.compile()
        # Assert the call of table to check the insertion of declaration
        self.assertEqual(self.table.enter_const.call_count, 2)
        self.assertEqual(self.table.enter_var.call_count, 2)
        self.assertEqual(self.table.enter_func.call_count, 2)
        # Assert the call of gen
        # `assert_has_calls` checks whether the actual call_list contains expected one.
        # In other words, check the appearance of call in the specified order.
        expected_gencode_v = [ call(OpCode.jmp, ANY), call(OpCode.jmp, ANY), call(OpCode.ict, ANY)
                             , call(OpCode.jmp, ANY), call(OpCode.ict, ANY), call(OpCode.ict, ANY) ]
        self.assertEqual(self.gen.gencode_v.call_count, 6)
        self.gen.gencode_v.assert_has_calls(expected_gencode_v)
        self.assertEqual(self.gen.gencode_r.call_count, 3)


    def test_compile_if(self):
        # Setup
        self.setUpReader('test/original3-2.pl')
        self.table.kind.return_value = IdKind.Var
        # Execute
        self.sut.compile()

        # print(self.table.mock_calls)
        # print(self.gen.mock_calls)

    def test_compile_while(self):
        # Setup
        self.setUpReader('test/original3-3.pl')
        self.table.kind.return_value = IdKind.Var
        # Execute
        self.sut.compile()
        # Assert
        expected_gencode_v = [ call(OpCode.jpc, ANY), ANY, call(OpCode.jmp, ANY) ]
        self.gen.gencode_v.assert_has_calls(expected_gencode_v)

    def test_compile_ret(self):
        # Setup
        self.setUpReader('test/original3-4.pl')
        self.table.kind.return_value = IdKind.Var
        # Execute
        self.sut.compile()
        # Assert
        expected_gencode_v = [ call(OpCode.lit, 1), call(OpCode.lit, 2) ]
        self.gen.gencode_v.assert_has_calls(expected_gencode_v)
        expected_gencode_o = [ call(Operator.add) ]
        self.gen.gencode_o.assert_has_calls(expected_gencode_o)
        self.assertEqual(self.gen.gencode_r.call_count, 2)

    def tearDown(self):
        self.sut.reader.close()

if __name__ == '__main__':
    main()
