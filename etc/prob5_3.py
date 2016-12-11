import sys

class Parser():
    '''
    Parse the below grammer.

    S -> '(', L, ')' | 'a'
    L -> S {, ',', S}
    '''
    def __init__(self, text):
        self.text = text
        self.token = None
        self.current_index = 0

    def parse(self):
        self.nextToken()
        self.parseS()

    def parseS(self):
        if self.token == '(':
            self.nextToken()
            self.parseL()
            if self.token == ')':
                self.nextToken()
            else:
                raise RuntimeError('illegal token: ' + self.token)
        elif self.token == 'a':
            self.nextToken()
        else:
            raise RuntimeError('illegal token: ' + self.token)

    def parseL(self):
        self.parseS()
        while self.token == ',':
            self.nextToken()
            self.parseS()

    def nextToken(self):
        if self.current_index >= len(self.text):
            return None
        self.token = self.text[self.current_index]
        self.current_index = self.current_index + 1
        return self.token

def traceit(frame, event, arg):
    if event == 'call':
        co_name = frame.f_code.co_name # name of functions
        print(co_name)
        if co_name == 'nextToken':
            print(frame.f_locals['self'].token)
    return traceit

if __name__ == '__main__':
    sys.settrace(traceit)

    print('parse: ', "'(a)'")
    parser = Parser('(a)')
    parser.parse()

    print('parse: ', "'(a,a,a)'")
    parser = Parser('(a,a,a)')
    parser.parse()

    print('parse: ', "'(a,(a,a),a)'")
    parser = Parser('(a,(a,a),a)')
    parser.parse()

    sys.settrace(None)

