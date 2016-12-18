from unittest import TestCase, main, skip
from unittest.mock import Mock, ANY, call
from compiler.table import IdKind, FuncEntry, ParEntry, VarEntry, ConstEntry, RelAddr, Pl0Table

class TestTable(TestCase):
    def setUp(self):
        self.sut = Pl0Table()

    def test_enter_var(self):
        # Execute
        self.sut.block_begin(2)
        self.sut.enter_var('x')
        self.sut.enter_var('y')
        self.sut.block_end()
        # Assert
        self.assertEqual(len(self.sut.table), 2)
        self.assertEqual(self.sut.table[0], VarEntry('x', RelAddr(0, 2)))
        self.assertEqual(self.sut.table[1], VarEntry('y', RelAddr(0, 3)))

    def test_enter_const(self):
        # Execute
        self.sut.block_begin(2)
        self.sut.enter_const('x', 1)
        self.sut.enter_const('y', 2)
        self.sut.block_end()
        # Assert
        self.assertEqual(len(self.sut.table), 2)
        self.assertEqual(self.sut.table[0], ConstEntry('x', 1))
        self.assertEqual(self.sut.table[1], ConstEntry('y', 2))

    def test_enter_func(self):
        # Execute
        self.sut.block_begin(2)
        ti = self.sut.enter_func('foo', 10)
        self.sut.block_begin(2)
        self.sut.enter_par('x')
        self.sut.enter_par('y')
        self.sut.end_par()
        self.sut.enter_var('a')
        self.sut.enter_var('b')
        self.sut.change_v(ti, 12)
        self.sut.block_end()
        self.sut.block_end()
        # Assert
        self.assertEqual(len(self.sut.table), 5)
        self.assertEqual(self.sut.table[0], FuncEntry('foo', RelAddr(0, 12), 2))
        self.assertEqual(self.sut.table[1], ParEntry('x', RelAddr(1, -2)))
        self.assertEqual(self.sut.table[2], ParEntry('y', RelAddr(1, -1)))
        self.assertEqual(self.sut.table[3], VarEntry('a', RelAddr(1, 2)))
        self.assertEqual(self.sut.table[4], VarEntry('b', RelAddr(1, 3)))

    def test_methods_to_get_info(self):
        # Execute
        self.sut.block_begin(2)
        # var
        self.sut.enter_var('x')
        # const
        self.sut.enter_const('y', 1)
        # func
        ti = self.sut.enter_func('foo', 10)
        self.sut.block_begin(2)
        self.sut.enter_par('x')
        self.sut.end_par()
        self.sut.enter_var('a')
        self.sut.change_v(ti, 12)
        self.sut.block_end()

        # Assert
        self.assertEqual(len(self.sut.table), 5)
        # kind
        self.assertEqual(self.sut.kind(0), IdKind.Var)
        self.assertEqual(self.sut.kind(1), IdKind.Const)
        self.assertEqual(self.sut.kind(2), IdKind.Func)
        # reladdr
        self.assertEqual(self.sut.reladdr(0), RelAddr(0, 2))
        # pars
        self.assertEqual(self.sut.pars(2), 1)
        # search
        self.assertEqual(self.sut.search('y', IdKind.Const), 1)
        self.assertEqual(self.sut.search('foo', IdKind.Func), 2)
        self.assertEqual(self.sut.search('nothing', IdKind.Func), -1)
        original_ti = self.sut.t_index
        self.sut.t_index = 1
        self.assertEqual(self.sut.search('x', IdKind.Var), 0)
        self.sut.t_index = 4
        self.assertEqual(self.sut.search('x', IdKind.Par), 3)
        self.sut.t_index = original_ti

    def tearDown(self):
        pass

if __name__ == '__main__':
    main()
