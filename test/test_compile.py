from unittest import TestCase, main, skip
from unittest.mock import Mock, ANY, call
from compiler.getsource import SourceReader
from compiler.table import IdKind, Pl0Table
from compiler.codegen import OpCode, Operator, Pl0CodeGenerator
from compiler.compile import Pl0Compiler

class TestCompile(TestCase):
    def setUp(self):
        pass

    def setUpReader(self, file_name):
        '''
        Set up Pl0Compiler.
        Use mocking for table and gen objects.
        '''
        self.reader = SourceReader(file_name)
        # `Mock` constructor ensures that the target class has methods which are actually called.
        # If not, AttributeError is raised.
        self.table = Mock(spec=Pl0Table)
        self.gen = Mock(spec=Pl0CodeGenerator)
        self.sut = Pl0Compiler(self.reader, self.table, self.gen)

    def test_compile_decl(self):
        # Setup
        self.setUpReader('test/compile_decl.pl')
        # Execute
        self.sut.compile()
        # Assert the call of table to check the insertion of declaration
        self.assertEqual(self.table.enter_const.call_count, 2)
        self.assertEqual(self.table.enter_var.call_count, 2)
        self.assertEqual(self.table.enter_func.call_count, 2)
        # Assert the call of gen
        # `assert_has_calls` checks whether the actual call_list contains expected one.
        # In other words, the assertion succeeds when the expected list is sublist of the actual one.
        expected_gencode_v = [ call(OpCode.jmp, ANY), call(OpCode.jmp, ANY), call(OpCode.ict, ANY)
                             , call(OpCode.jmp, ANY), call(OpCode.ict, ANY), call(OpCode.ict, ANY) ]
        self.assertEqual(self.gen.gencode_v.call_count, 6)
        self.gen.gencode_v.assert_has_calls(expected_gencode_v)
        self.assertEqual(self.gen.gencode_r.call_count, 3)


    def test_compile_if(self):
        # Setup
        self.setUpReader('test/compile_if.pl')
        self.table.kind.return_value = IdKind.Var
        # Execute
        self.sut.compile()
        # Assert
        self.gen.gencode_v.assert_any_call(OpCode.jpc, ANY)
        self.gen.backpatch.assert_any_call(ANY)

    def test_compile_while(self):
        # Setup
        self.setUpReader('test/compile_while.pl')
        self.table.kind.return_value = IdKind.Var
        # Execute
        self.sut.compile()
        # Assert
        expected_gencode_v = [ call(OpCode.jpc, ANY), ANY, call(OpCode.jmp, ANY) ]
        self.gen.gencode_v.assert_has_calls(expected_gencode_v)

    def test_compile_ret(self):
        # Setup
        self.setUpReader('test/compile_ret.pl')
        self.table.kind.return_value = IdKind.Var
        # Execute
        self.sut.compile()
        # Assert
        expected_gencode_v = [ call(OpCode.lit, 1), call(OpCode.lit, 2) ]
        self.gen.gencode_v.assert_has_calls(expected_gencode_v)
        expected_gencode_o = [ call(Operator.add) ]
        self.gen.gencode_o.assert_has_calls(expected_gencode_o)
        self.assertEqual(self.gen.gencode_r.call_count, 2)

    def test_compile_write(self):
        # Setup
        self.setUpReader('test/compile_write.pl')
        self.table.kind.return_value = IdKind.Var
        # Execute
        self.sut.compile()
        # Assert
        self.gen.gencode_o.assert_any_call(Operator.wrt)
        self.gen.gencode_o.assert_any_call(Operator.wrl)

    def test_compile_expr1(self):
        # Setup
        self.setUpReader('test/compile_expr1.pl')
        self.table.kind.return_value = IdKind.Var
        # Execute
        self.sut.compile()
        # Assert
        expected_gencode_o = [ call(Operator.neg), call(Operator.add), call(Operator.add) ]
        self.gen.gencode_o.assert_has_calls(expected_gencode_o)

    def test_compile_expr2(self):
        # Setup
        self.setUpReader('test/compile_expr2.pl')
        self.table.kind.return_value = IdKind.Var
        # Execute
        self.sut.compile()
        # Assert
        expected_gencode_o = [ call(Operator.mul), call(Operator.mul), call(Operator.add),
                               call(Operator.div), call(Operator.add) ]
        self.assertEqual(self.gen.gencode_o.mock_calls, expected_gencode_o)

    def test_compile_condition(self):
        # Setup
        self.setUpReader('test/compile_condition.pl')
        self.table.kind.return_value = IdKind.Var
        # Execute
        self.sut.compile()
        # Assert
        self.gen.gencode_o.assert_any_call(Operator.odd)
        self.gen.gencode_o.assert_any_call(Operator.eq)
        self.gen.gencode_o.assert_any_call(Operator.ls)
        self.gen.gencode_o.assert_any_call(Operator.gr)
        self.gen.gencode_o.assert_any_call(Operator.neq)
        self.gen.gencode_o.assert_any_call(Operator.lseq)
        self.gen.gencode_o.assert_any_call(Operator.greq)

    def tearDown(self):
        if hasattr(self, 'sut'):
            self.sut.reader.close()

if __name__ == '__main__':
    main()
