from enum import Enum, unique

@unique
class IdKind(Enum):
    Var = 1
    Func = 2
    Par = 3
    Const = 4

class RelAddr:
    def __init__(self, level, addr):
        self.level = level
        self.addr = addr

    def __str__(self):
        return "RelAddr {level=%d, addr=%d}" % (self.level, self.addr)

    def __repr__(self):
        return "RelAddr {level=%d, addr=%d}" % (self.level, self.addr)

class Entry:
    def __init__(self, kind, name):
        self.kind = kind
        self.name = name

class VarEntry(Entry):
    def __init__(self, name, raddr):
        super().__init__(IdKind.Var, name)
        self.raddr = raddr

    def __str__(self):
        return "VarEntry {kind=%s, name=%s, raddr=%s}" % (str(self.kind), self.name, str(self.raddr))

    def __repr__(self):
        return "VarEntry {kind=%s, name=%s, raddr=%s}" % (str(self.kind), self.name, str(self.raddr))

class FuncEntry(Entry):
    def __init__(self, name, raddr, pars):
        super().__init__(IdKind.Func, name)
        self.raddr = raddr
        self.pars = pars

    def __str__(self):
        return "FuncEntry {kind=%s, name=%s, raddr=%s, pars=%d}" % (str(self.kind), self.name, str(self.raddr), self.pars)

    def __repr__(self):
        return "FuncEntry {kind=%s, name=%s, raddr=%s, pars=%d}" % (str(self.kind), self.name, str(self.raddr), self.pars)

class ParEntry(Entry):
    def __init__(self, name, raddr):
        super().__init__(IdKind.Par, name)
        self.raddr = raddr

    def __str__(self):
        return "ParEntry {kind=%s, name=%s, raddr=%s}" % (str(self.kind), self.name, str(self.raddr))

    def __repr__(self):
        return "ParEntry {kind=%s, name=%s, raddr=%s}" % (str(self.kind), self.name, str(self.raddr))

class ConstEntry(Entry):
    def __init__(self, name, value):
        super().__init__( IdKind.Const, name)
        self.value = value

    def __str__(self):
        return "ConstEntry {kind=%s, name=%s, value=%d}" % (str(self.kind), self.name, self.value)

    def __repr__(self):
        return "ConstEntry {kind=%s, name=%s, value=%d}" % (str(self.kind), self.name, self.value)

class Pl0Table:
    def __init__(self):
        self.table = []
        self.t_index = None
        self.level = None
        self.local_addr = None
        self.tf_Index = None
        self.index = []
        self.addr = []

    def block_begin(self, first_addr):
        if self.level is None:
            self.local_addr = first_addr
            self.t_index = 0
            self.level = 0
        else:
            self.index[self.level] = self.t_index
            self.addr[self.level] = self.local_addr
            self.local_addr = first_addr
            self.level += 1

    def block_end(self):
        self.level -= 1
        self.t_index = self.index[self.level]
        self.local_addr = self.addr[self.level]

    def b_level(self):
        return self.level

    def f_pars(self):
        return self.table[self.index[self.level-1]].pars

    def enter_func(self, id_, v):
        pass

    def enter_var(self, id_):
        pass

    def enter_par(self, id_):
        pass

    def enter_const(self, id_, v):
        pass

    def end_par(self):
        pass

    def change_v(self, ti, new_val):
        pass

    def frame_l(self):
        pass

    def search(self, id_, k):
        pass

    def kind(self, i):
        pass

    def pars(self, ti):
        pass
