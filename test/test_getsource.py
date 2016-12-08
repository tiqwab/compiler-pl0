import unittest
import sys
from compiler.getsource import SourceReader

'''
Execute `python setup.py test` to test all cases
'''

class TestGetSource(unittest.TestCase):

    def test_next_char(self):
        sut = SourceReader('test/original1.pl')
        result = []

        try:
            while True:
                c = sut.next_char()
                if c is None:
                    break
                result.append(c)
        finally:
            sut.close()

        sut.close()
        self.assertEqual(''.join(result), "onetwothree four")

if __name__ == '__main__':
    unittest.main()
