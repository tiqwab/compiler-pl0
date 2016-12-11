from compiler.getsource import Token, SourceReader
from compiler.codegen import OpCode

FIRSTADDR = 2

class Pl0Compiler:
    '''
    Analyze syntax and translate to codes for a stack machine.
    '''
    def __init__(self, reader, table, gen):
        self.reader = reader # SourceReader
        self.table = table # Pl0Table
        self.gen = gen # Pl0CodeGenerator
        self.token = None

    def next_token(self):
        self.token = self.reader.next_token()

    def compile(self):
        self.next_token()
        self.table.block_begin(FIRSTADDR)
        self.block(0) # argument 0 is dummy

    def block(self, p_index):
        backp = gen.gencode_v(OpCode.jmp, 0)
        while True:
            if self.token.kind == Const:
                pass
            elif self.token.kind == Var:
                pass
            elif self.token.kind == Func:
                pass
            else:
                break
        gen.backpatch(backp)
        self.table.change_v(p_index, self.gen.next_code())
        self.gen.gencode_v(OpCode.ict, self.table.frame_l())
        self.statement()
        self.gen.gencode_r()
        self.table.block_end()

    def const_decl(self):
        pass

    def var_decl(self):
        pass

    def func_decl(self):
        pass

    def statement(self):
        pass
