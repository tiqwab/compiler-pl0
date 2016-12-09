import string
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
    Lparen    = "("
    Rparen    = ")"
    Equal     = "="
    Lss       = "<"
    Gtr       = ">"
    NotEq     = "<>"
    LssEq     = "<="
    GtrEq     = ">="
    Comma     = ","
    Period    = "."
    Semicolon = ";"
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
    def to_keywd(self, token):
        for x in KeyWd:
            if x.value == token:
                return x
        return None

    @classmethod
    def is_keysym(self, token):
        return token in [x.value for x in KeySym.__members__.values()]

    @classmethod
    def to_kind(self, chara):
        # FIXME
        if chara == "":
            return KeyEtc.Others

        if chara in string.digits:
            return KeyEtc.Digit
        elif chara in string.ascii_letters:
            return KeyEtc.Letter
        elif chara == '+':
            return KeySym.Plus
        elif chara == '-':
            return KeySym.Minus
        elif chara == '*':
            return KeySym.Mult
        elif chara == '/':
            return KeySym.Div
        elif chara == '(':
            return KeySym.Lparen
        elif chara == ')':
            return KeySym.Rparen
        elif chara == '=':
            return KeySym.Equal
        elif chara == '<':
            return KeySym.Lss
        elif chara == '>':
            return KeySym.Gtr
        elif chara == ',':
            return KeySym.Comma
        elif chara == '.':
            return KeySym.Period
        elif chara == ';':
            return KeySym.Semicolon
        elif chara == ':':
            return KeyEtc.Colon
        else:
            return KeyEtc.Others

    @classmethod
    def is_space(self, chara):
        return chara == ' ' or chara == '\t'

class Token:
    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

    def __str__(self):
        return "Token {kind=%s, value=%s}" % (self.kind, repr(self.value))

    def __repr__(self):
        return "Token {kind=%s, value=%s}" % (self.kind, repr(self.value))

class SourceReader:
    def __init__(self, input_file):
        self.input_file = open(input_file, 'r')
        self.line = None
        self.line_index = 0
        self.ch = None 

    def next_char(self):
        if self.line == None:
            self.line = self.input_file.readline()
            if self.line == "":
                self.line = None
                return ""
            self.line_index = 0

        c = self.line[self.line_index]
        self.line_index += 1
        if self.line_index >= len(self.line):
            self.line = None
        return c

    def next_token(self):
        # first reading or spaces
        while self.ch == None or KeyTable.is_space(self.ch):
            self.ch = self.next_char()

        kind = KeyTable.to_kind(self.ch)
        if kind == KeyEtc.Letter:
            ident = self.ch
            self.ch = self.next_char()
            while KeyTable.to_kind(self.ch) in [KeyEtc.Letter, KeyEtc.Digit]:
                ident += self.ch
                self.ch = self.next_char()
            # when ident is keywd
            if KeyTable.is_keywd(ident):
                token = Token(KeyTable.to_keywd(ident))
            # when ident is not keywd, such as name of variables
            else:
                token = Token(KeyToken.Id, ident) 
        elif kind == KeyEtc.Digit:
            token = Token(kind, self.ch)
            self.ch = self.next_char()
        elif kind == KeyEtc.Colon:
            token = Token(kind, self.ch)
            self.ch = self.next_char()
        elif kind == KeySym.Lss:
            token = Token(kind, self.ch)
            self.ch = self.next_char()
        elif kind == KeySym.Gtr:
            token = Token(kind, self.ch)
            self.ch = self.next_char()
        else:
            token = Token(kind, self.ch)
            self.ch = self.next_char()
        return token

    def close(self):
        self.input_file.close()

