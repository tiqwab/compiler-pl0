import sys
from io import StringIO
from unittest import TestCase, main
from compiler.getsource import SourceReader
from compiler.table import Pl0Table
from compiler.codegen import Pl0CodeGenerator
from compiler.compile import Pl0Compiler

class TestIntegrate(TestCase):
    def setUp(self):
        self.sut = None
        self.buf = StringIO()
        sys.stdout = self.buf

    def test_compile_and_execute(self):
        '''
        Test to compile a original source and execute the produced target codes.
        Assertion checks the output of execution by replacing stdout to StringIO.
        '''
        # Setup
        self.sut = self.setUpCompiler('test/integrate1.pl')
        # Execute
        self.sut.compile()
        self.sut.gen.execute()
        # Assert
        self.assertEqual(self.buf.getvalue(), '785595\n84361212\n27\n')

    def tearDown(self):
        sys.stdout = sys.__stdout__
        if self.sut is not None:
            self.sut.reader.close()

    def setUpCompiler(self, file_name):
        reader = SourceReader(file_name)
        table = Pl0Table()
        gen = Pl0CodeGenerator(table)
        return Pl0Compiler(reader, table, gen)
