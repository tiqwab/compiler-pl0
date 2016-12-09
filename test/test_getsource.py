import unittest
import sys
from compiler.getsource import KeyEtc, SourceReader

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
                if c == "":
                    break
                result.append(c)
        finally:
            sut.close()

        self.assertEqual(''.join(result), "onetwothree four")

    def test_next_token(self):
        sut = SourceReader('test/original2.pl')

        try:
            while True:
                token = sut.next_token()
                print(token)
                if token.kind == KeyEtc.Others:
                    break
        finally:
            sut.close()

if __name__ == '__main__':
    unittest.main()
