from unittest import TestCase, main
from unittest.mock import Mock, ANY, call
from compiler.getsource import SourceReader
from compiler.table import Pl0Table
from compiler.codegen import OpCode, Pl0CodeGenerator
from compiler.compile import Pl0Compiler

class TestCompile(TestCase):
    def setUp(self):
        pass

    def setUpReader(self, file_name):
        self.reader = SourceReader(file_name)
        self.table = Mock(spec=Pl0Table)
        self.gen = Mock(spec=Pl0CodeGenerator)
        self.sut = Pl0Compiler(self.reader, self.table, self.gen)

    def test_compile(self):
        # Setup
        self.setUpReader('test/original3.pl')
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

    def tearDown(self):
        self.sut.reader.close()

if __name__ == '__main__':
    main()
