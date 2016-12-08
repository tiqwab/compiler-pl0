from enum import Enum, unique

MAXLINE = 120

@unique # Assert that values of enum are different from each other
class KeyWd(Enum):
    Begin   = "begin"
    End     = "end"
    If      = "if"
    Then    = "then"
    While   = "while"
    Do      = "do"
    Ret     = "return"
    Func    = "function"
    Var     = "var"
    Const   = "const"
    Odd     = "odd"
    Write   = "write"
    WriteLn = "writeln"

@unique
class KeySym(Enum):
    Plus      = "+"
    Minus     = "-"
    Mult      = "*"
    Div       = "/"
    LParen    = "("
    RParen    = ")"
    Equal     = "="
    Lss       = "<"
    Gtr       = ">"
    NotEq     = "<>"
    LssEq     = "<="
    GtrEq     = ">="
    Comma     = ","
    Period    = "."
    SemiColon = ";"
    Assign    = ":="

@unique
class KeyToken(Enum):
    Id  = "id"
    Num = "num"
    Nul = "nul"

@unique
class KeyEtc(Enum):
    Letter = "letter"
    Digit  = "digit"
    Colon  = "colon"
    Others = "others"

class KeyTable:
    @classmethod
    def is_keywd(self, token):
        return token in [x.value for x in KeyWd.__members__.values()]

    @classmethod
    def is_keysym(self, token):
        return token in [x.value for x in KeySym.__members__.values()]

class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

class SourceReader:
    def __init__(self, input_file):
        self.input_file = open(input_file, 'r')
        self.line = None
        self.line_index = 0

    def next_char(self):
        if self.line == None:
            self.line = self.input_file.readline().strip()
            if self.line == "":
                return None
            self.line_index = 0

        c = self.line[self.line_index]
        self.line_index += 1
        if self.line_index >= len(self.line):
            self.line = None
        return c

    def close(self):
        self.input_file.close()

