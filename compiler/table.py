from enum import Enum, unique

@unique
class IdKind(Enum):
    Var = 1
    Func = 2
    Par = 3
    Const = 4

class Pl0Table:
    def __init__(self):
        pass

    def block_begin(self, first_addr):
        pass

    def block_end(self):
        pass

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
