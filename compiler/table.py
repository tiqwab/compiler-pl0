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

    def __eq__(self, other):
        if other is None or not isinstance(other, RelAddr):
            return False
        return self.level == other.level and self.addr == other.addr

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

    def __eq__(self, other):
        if other is None or not isinstance(other, VarEntry):
            return False
        return self.kind == other.kind and self.name == other.name and self.raddr == other.raddr

class FuncEntry(Entry):
    def __init__(self, name, raddr, pars=0):
        super().__init__(IdKind.Func, name)
        self.raddr = raddr
        self.pars = pars # pars is incremented in Pl0Table#enter_par

    def __str__(self):
        return "FuncEntry {kind=%s, name=%s, raddr=%s, pars=%d}" % (str(self.kind), self.name, str(self.raddr), self.pars)

    def __repr__(self):
        return "FuncEntry {kind=%s, name=%s, raddr=%s, pars=%d}" % (str(self.kind), self.name, str(self.raddr), self.pars)

    def __eq__(self, other):
        if other is None or not isinstance(other, FuncEntry):
            return False
        return self.kind == other.kind and self.name == other.name and self.raddr == other.raddr and self.pars == other.pars

class ParEntry(Entry):
    def __init__(self, name, raddr):
        super().__init__(IdKind.Par, name)
        self.raddr = raddr

    def __str__(self):
        return "ParEntry {kind=%s, name=%s, raddr=%s}" % (str(self.kind), self.name, str(self.raddr))

    def __repr__(self):
        return "ParEntry {kind=%s, name=%s, raddr=%s}" % (str(self.kind), self.name, str(self.raddr))

    def __eq__(self, other):
        if other is None or not isinstance(other, ParEntry):
            return False
        return self.kind == other.kind and self.name == other.name and self.raddr == other.raddr

class ConstEntry(Entry):
    def __init__(self, name, value):
        super().__init__( IdKind.Const, name)
        self.value = value

    def __str__(self):
        return "ConstEntry {kind=%s, name=%s, value=%d}" % (str(self.kind), self.name, self.value)

    def __repr__(self):
        return "ConstEntry {kind=%s, name=%s, value=%d}" % (str(self.kind), self.name, self.value)

    def __eq__(self, other):
        if other is None or not isinstance(other, ConstEntry):
            return False
        return self.kind == other.kind and self.name == other.name and self.value == other.value

class Pl0Table:
    def __init__(self):
        self.table = []
        self.t_index = None
        self.level = None
        self.local_addr = None
        self.tf_index = None
        self.index = []
        self.addr = []

    def enter(self, entry):
        self.t_index += 1
        if len(self.table) == self.t_index:
            self.table.append(entry)
        elif len(self.table) > self.t_index:
            self.table[t_index] = entry
        else:
            raise RuntimeError("illegal index: " + self.t_index)

    def block_begin(self, first_addr):
        if self.level is None:
            self.local_addr = first_addr
            self.t_index = -1
            self.level = 0
        else:
            # self.index[self.level] = self.t_index
            # self.addr[self.level] = self.local_addr
            self.index.append(self.t_index)
            self.addr.append(self.local_addr)
            self.local_addr = first_addr
            self.level += 1

    def block_end(self):
        self.level -= 1
        if self.level >= 0:
            self.t_index = self.index[self.level]
            self.local_addr = self.addr[self.level]

    def b_level(self):
        return self.level

    def f_pars(self):
        entry = self.table[self.index[self.level-1]]
        assert isinstance(entry, FuncEntry) == True
        return entry.pars

    def enter_func(self, id_, addr):
        self.enter(FuncEntry(id_, RelAddr(self.level, addr)))
        self.tf_index = self.t_index
        return self.t_index

    def enter_par(self, id_):
        self.enter(ParEntry(id_, RelAddr(self.level, None)))
        self.table[self.tf_index].pars += 1
        return self.t_index

    def enter_var(self, id_):
        self.enter(VarEntry(id_, RelAddr(self.level, self.local_addr)))
        self.local_addr += 1
        return self.t_index

    def enter_const(self, id_, value):
        self.enter(ConstEntry(id_, value))
        return self.t_index

    def end_par(self):
        entry = self.table[self.tf_index]
        assert isinstance(entry, FuncEntry) == True
        pars = entry.pars
        for i in range(0, pars):
            self.table[self.tf_index+i+1].raddr.addr = i-pars

    def change_v(self, ti, new_addr):
        entry = self.table[ti]
        assert isinstance(entry, FuncEntry) == True
        entry.raddr.addr = new_addr

    def search(self, id_, k):
        i = self.t_index
        for i in range(i, -1, -1):
            if id_ == self.table[i].name:
                return i
        if k == IdKind.Var:
            return self.enter_var(id_)
        return 0

    def kind(self, i):
        return self.table[i].kind

    def reladdr(self, ti):
        entry = self.table[ti]
        assert isinstance(entry, VarEntry) == True \
                or isinstance(entry, FuncEntry) == True \
                or isinstance(entry, ParEntry) == True
        return entry.raddr

    def val(self, ti):
        entry = self.table[ti]
        assert isinstance(entry, ConstEntry) == True
        return entry.value

    def pars(self, ti):
        entry = self.table[ti]
        assert isinstance(entry, FuncEntry) == True
        return entry.pars

    def frame_l(self):
        return self.local_addr

