import itertools
from enum import Enum, unique

MAX_TABLE = 100
MAX_LEVEL = 5

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
    '''
    Entry of variables.
    name: the name of variables.
    raddr.level: the level of variables
    raddr.addr: the relative addr from the beginning of function.
                For example, 3 if this is the first variable in the block.
    '''
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
    '''
    Entry of functions.
    name: the name of function
    raddr.level: the level of the function name (not the inside of the function).
    raddr.addr: the index of target codes which starts function's process
    pars: the num or parameters of function
    '''
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
    '''
    Entry of parameters of functions.
    name: the name of parameter
    raddr.level: the level of parameter
    raddr.addr: the relative addr from the beginning of function.
                For example, -1 if this is the last param of function.
    '''
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
    '''
    Entry of constant values.
    name: the name of constant
    value: the value of constant
    '''
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
    '''
    Symbol table for Pl0 compiler.
    '''
    def __init__(self):
        self.table = [x for x in itertools.repeat(None, MAX_TABLE)]
        self.table[0] = FuncEntry('dummy', RelAddr(0, 0))
        self.t_index = None
        self.level = None # Level of blocks. Incremented when enter new blocks.
        self.local_addr = None # Set at the beginning and end of the block. 2 + the num of local variables of the block
        self.tf_index = None # Index of the function of the table. Set when enter the declaration of functions.
        self.index = [x for x in itertools.repeat(0, MAX_LEVEL)]
        self.addr = [x for x in itertools.repeat(0, MAX_LEVEL)]

    def enter(self, entry):
        self.t_index += 1
        if len(self.table) == self.t_index:
            self.table.append(entry)
        elif len(self.table) > self.t_index:
            self.table[self.t_index] = entry
        else:
            raise RuntimeError("illegal index: " + str(self.t_index))

    def block_begin(self, first_addr):
        if self.level is None:
            self.local_addr = first_addr
            self.t_index = 0
            self.level = 0
        else:
            self.index[self.level] = self.t_index # save t_index temporarily
            self.addr[self.level] = self.local_addr # save local_addr temporarily
            self.local_addr = first_addr
            self.level += 1

    def block_end(self):
        self.level -= 1
        if self.level >= 0:
            self.t_index = self.index[self.level] # recover t_index
            self.local_addr = self.addr[self.level] # recover local_addr

    def b_level(self):
        return self.level

    def f_pars(self):
        '''
        Return the number of arguments of functions.
        `f_pars` is called when generate `ret` op, indicating that the value of `level` is for the inside of the function, so use `level-1` to retrieve entry.
        '''
        entry = self.table[self.index[self.level-1]]
        assert isinstance(entry, FuncEntry)
        return entry.pars

    def enter_func(self, id_, addr):
        '''
        Enter a new FuncEntry.
        `pars` and actual `addr` will be set later.
        '''
        self.enter(FuncEntry(id_, RelAddr(self.level, addr)))
        self.tf_index = self.t_index
        return self.t_index

    def enter_par(self, id_):
        '''
        Enter a new ParEntry.
        `addr` will be set later in `end_par`.
        '''
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
        assert isinstance(entry, FuncEntry)
        pars = entry.pars
        # update addr of each parameter of the function
        for i in range(0, pars):
            self.table[self.tf_index+i+1].raddr.addr = i-pars

    def change_v(self, ti, new_addr):
        entry = self.table[ti]
        assert isinstance(entry, FuncEntry)
        entry.raddr.addr = new_addr

    def search(self, id_, k):
        l = self.t_index
        for i in range(l, -1, -1):
            if id_ == self.table[i].name:
                return i
        # if k == IdKind.Var:
        #     return self.enter_var(id_)
        raise RuntimeError("unknown var or function: " + id_)

    def kind(self, i):
        return self.table[i].kind

    def reladdr(self, ti):
        entry = self.table[ti]
        assert isinstance(entry, VarEntry) \
                or isinstance(entry, FuncEntry) \
                or isinstance(entry, ParEntry)
        return entry.raddr

    def val(self, ti):
        entry = self.table[ti]
        assert isinstance(entry, ConstEntry)
        return entry.value

    def pars(self, ti):
        entry = self.table[ti]
        assert isinstance(entry, FuncEntry)
        return entry.pars

    def frame_l(self):
        return self.local_addr

