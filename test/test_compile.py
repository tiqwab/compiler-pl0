import unittest
from compiler.getsource import SourceReader
from compiler.table import Pl0Table
from compiler.codegen import Pl0CodeGenerator
from compiler.compile import Pl0Compiler

class TestCompile(unittest.TestCase):
    def setUp(self):
        reader = SourceReader('test/original3.pl')
        table = Pl0Table()
        gen = Pl0CodeGenerator()
        self.sut = Pl0Compiler(reader, table, gen)

    def test_compile(self):
        self.sut.compile()

    def tearDown(self):
        self.sut.reader.close()

if __name__ == '__main__':
    unittest.main()
