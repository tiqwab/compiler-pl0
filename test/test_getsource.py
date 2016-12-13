import unittest
import string
import sys
from compiler.getsource import KeyWd, KeySym, KeyToken, KeyEtc, KeyTable, Token, SourceReader

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

        self.assertEqual(''.join(result), "one\ntwo\nthree four\n")

    def to_any_kind(self, k):
        for x in KeyWd:
            if k == x.name:
                return x
        for x in KeySym:
            if k == x.name:
                return x
        for x in KeyToken:
            if k == x.name:
                return x
        return None

    def test_next_token(self):
        sut = SourceReader('test/original2.pl')
        tokens = []

        try:
            while True:
                token = sut.next_token()
                tokens.append(token)
                if token.kind == KeyEtc.Others and token.value == "":
                    break
        finally:
            sut.close()

        expected = []
        with open('test/original2.expect', 'r') as f:
            for line in f.readlines():
                line = line.strip()
                xs = line.split(' ', 1)
                if len(xs) > 1:
                    kind = xs[0]
                    val = xs[1]
                    if val.isdigit():
                        val = int(val)
                else:
                    kind = xs[0]
                    val = None
                expected.append(Token(self.to_any_kind(kind), val))
        expected.append(Token(KeyEtc.Others, ''))
        self.assertEqual(tokens, expected)

if __name__ == '__main__':
    unittest.main()
