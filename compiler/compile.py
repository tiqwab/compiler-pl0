from compiler.getsource import KeyWd, KeySym, KeyToken, Token, SourceReader
from compiler.codegen import OpCode, Operator
from compiler.table import IdKind

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
        token = self.reader.next_token()
        self.token = token
        return token

    def check_get(self, token, kind):
        '''
        Check kind of the token and read next_token.
        Raise error when the actual kind is not the specified one.
        '''
        if token.kind == kind:
            self.next_token()
        else:
            raise RuntimeError("expect:" + kind.name + ", but actual:" + token.kind.name)

    def compile(self):
        self.next_token()
        self.table.block_begin(FIRSTADDR)
        self.block(0) # argument 0 is dummy

    def block(self, p_index):
        backp = self.gen.gencode_v(OpCode.jmp, 0)
        while True:
            if self.token.kind == KeyWd.Const:
                self.next_token()
                self.const_decl()
            elif self.token.kind == KeyWd.Var:
                self.next_token()
                self.var_decl()
            elif self.token.kind == KeyWd.Func:
                self.next_token()
                self.func_decl()
            else:
                break
        self.gen.backpatch(backp)
        self.table.change_v(p_index, self.gen.next_code())
        self.gen.gencode_v(OpCode.ict, self.table.frame_l())
        self.statement()
        self.gen.gencode_r()
        self.table.block_end()

    def const_decl(self):
        while True:
            if self.token.kind == KeyToken.Id:
                temp = self.token
                self.check_get(self.next_token(), KeySym.Equal)
                if self.token.kind == KeyToken.Num:
                    self.table.enter_const(temp.value, self.token.value)
                else:
                    raise RuntimeError("expected number, but: " + self.token.kind.name)
                self.next_token()
            else:
                raise RuntimeError("expected Id, but: " + self.token.kind.name)
            if self.token.kind != KeySym.Comma:
                break
            self.next_token()
        self.check_get(self.token, KeySym.Semicolon)

    def var_decl(self):
        while True:
            if self.token.kind == KeyToken.Id:
                self.table.enter_var(self.token.value)
                self.next_token()
            else:
                raise RuntimeError("expected Id, but: " + self.token.kind.name)
            if self.token.kind != KeySym.Comma:
                break
            self.next_token()
        self.check_get(self.token, KeySym.Semicolon)

    def func_decl(self):
        if self.token.kind != KeyToken.Id:
            raise RuntimeError("expected Id, but: " + self.token.kind.name)

        f_index = self.table.enter_func(self.token.value, self.gen.next_code())
        self.check_get(self.next_token(), KeySym.Lparen)
        self.table.block_begin(FIRSTADDR)
        while True:
            if self.token.kind == KeyToken.Id:
                self.table.enter_par(self.token.value)
                self.next_token()
            else:
                break
            if self.token.kind != KeySym.Comma:
                break
            self.next_token()
        self.check_get(self.token, KeySym.Rparen)
        self.table.end_par()

        # if self.token.kind == KeySym.Semicolon:
        #     self.next_token()
        self.block(f_index)
        self.check_get(self.token, KeySym.Semicolon)

    def statement(self):
        while True:
            if self.token.kind == KeyToken.Id:
                t_index = self.table.search(self.token.value, IdKind.Var)
                k = self.table.kind(t_index)
                if k != IdKind.Var and k != IdKind.Par:
                    raise RuntimeError("unexpected id: " + str(k))
                self.check_get(self.next_token(), KeySym.Assign)
                self.expression()
                self.gen.gencode_t(OpCode.sto, t_index)
                return
            elif self.token.kind == KeyWd.If:
                self.next_token()
                self.condition()
                self.check_get(self.token, KeyWd.Then)
                back_p = self.gen.gencode_v(OpCode.jpc, 0)
                self.statement()
                self.gen.backpatch(back_p)
                return
            elif self.token.kind == KeyWd.Ret:
                self.next_token()
                self.expression()
                self.gen.gencode_r()
                return
            elif self.token.kind == KeyWd.Begin:
                self.next_token()
                while True:
                    self.statement()
                    # continue reading when ';' is found, stop reading when 'end', otherwise raise error
                    if self.token.kind == KeySym.Semicolon:
                        self.next_token()
                    if self.token.kind == KeyWd.End:
                        self.next_token()
                        return
                    # raise RuntimeError("unexpected token: " + str(self.token))
            elif self.token.kind == KeyWd.While:
                self.next_token()
                backp2 = self.gen.next_code()
                self.condition()
                self.check_get(self.token, KeyWd.Do)
                backp = self.gen.gencode_v(OpCode.jpc, 0)
                self.statement()
                self.gen.gencode_v(OpCode.jmp, backp2)
                self.gen.backpatch(backp)
                return
            elif self.token.kind == KeyWd.Write:
                self.next_token()
                self.expression()
                self.gen.gencode_o(Operator.wrt)
                return
            elif self.token.kind == KeyWd.WriteLn:
                self.next_token()
                self.gen.gencode_o(Operator.wrl)
                return
            elif self.token.kind == KeyWd.End:
                self.next_token()
                return
            elif self.token.kind == KeySym.Semicolon:
                self.next_token()
                return
            elif self.token.kind == KeySym.Period:
                self.next_token()
                return
            else:
                raise RuntimeError("unexpected token: " + str(self.token))

    def expression(self):
        prev_token = self.token
        if prev_token.kind in [KeySym.Plus, KeySym.Minus]:
            # for unary operators
            self.next_token()
            self.term()
            if prev_token.kind == KeySym.Minus:
                self.gen.gencode_o(Operator.neg)
        else:
            self.term()
        prev_token = self.token
        while prev_token.kind in [KeySym.Plus, KeySym.Minus]:
            self.next_token()
            self.term()
            if prev_token.kind == KeySym.Plus:
                self.gen.gencode_o(Operator.add)
            else:
                self.gen.gencode_o(Operator.sub)
            prev_token = self.token

    def term(self):
        self.factor()
        prev_token = self.token
        while prev_token.kind in [KeySym.Mult, KeySym.Div]:
            self.next_token()
            self.factor()
            if prev_token.kind == KeySym.Mult:
                self.gen.gencode_o(Operator.mul)
            else:
                self.gen.gencode_o(Operator.div)
            prev_token = self.token

    def factor(self):
        if self.token.kind == KeyToken.Id:
            t_index = self.table.search(self.token.value, IdKind.Var)
            kind = self.table.kind(t_index)
            if kind in [IdKind.Var, IdKind.Par]:
                self.gen.gencode_t(OpCode.lod, t_index)
                self.next_token()
            elif kind == IdKind.Const:
                self.gen.gencode_v(OpCode.lit, t_index)
                self.next_token()
            elif kind == IdKind.Func:
                self.next_token()
                if self.token.kind != KeySym.Lparen:
                    raise RuntimeError("expect Lparen, but actual is : " + str(self.token))

                self.next_token()
                if self.token.kind != KeySym.Rparen:
                    i = 0
                    while True:
                        self.expression()
                        i += 1
                        if self.token.kind == KeySym.Comma:
                            self.next_token()
                        else:
                            self.check_get(self.token, KeySym.Rparen)
                            break
                else:
                    self.next_token()

                if self.table.pars(t_index) != i:
                    raise RuntimeError("expect %d pars, but actual is %d" % (self.table.pars(t_index), i))
                self.gen.gencode_t(OpCode.cal, t_index)
            else:
                raise RuntimeError("unexpected IdKind: " + str(kind))
        elif self.token.kind == KeyToken.Num:
            self.gen.gencode_v(OpCode.lit, self.token.value)
            self.next_token()
        elif self.token.kind == KeySym.Lparen:
            self.next_token()
            self.expression()
            self.check_get(self.token, KeySym.Rparen)

        if self.token.kind in [KeyToken.Id, KeyToken.Num, KeySym.Lparen]:
            raise RuntimeError("unexpected token: " + str(self.token))

    def code_o(self, op):
        '''
        just for `condition` method
        '''
        self.next_token()
        self.expression()
        self.gen.gencode_o(op)

    def condition(self):
        if self.token.kind == KeyWd.Odd:
            self.code_o(Operator.odd)
            return

        self.expression()
        kind = self.token.kind
        if kind == KeySym.Equal:
            self.code_o(Operator.eq)
        elif kind == KeySym.Lss:
            self.code_o(Operator.ls)
        elif kind == KeySym.Gtr:
            self.code_o(Operator.gr)
        elif kind == KeySym.NotEq:
            self.code_o(Operator.neq)
        elif kind == KeySym.LssEq:
            self.code_o(Operator.lseq)
        elif kind == KeySym.GtrEq:
            self.code_o(Operator.greq)
        else:
            raise RuntimeError("unexpected token: " + str(token))
