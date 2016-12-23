import sys
from compiler.compile import Pl0Compiler
from compiler.getsource import SourceReader
from compiler.table import Pl0Table
from compiler.codegen import Pl0CodeGenerator

def main(file_name):
    reader = SourceReader(file_name)
    table = Pl0Table()
    gen = Pl0CodeGenerator(table)
    compiler = Pl0Compiler(reader, table, gen)

    compiler.compile()

    # Print symtable
    #print(table.table)
    # Format and print codes
    #for col, code in zip(range(0, len(gen.codes)), gen.codes):
    #    print("%d: %s" % (col, code))

    gen.execute()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = 'resources/sample1.pl'
    main(file_name)
