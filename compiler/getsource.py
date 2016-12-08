MAXLINE = 120

class SourceReader:
    def __init__(self, input_file):
        self.input_file = open(input_file, 'r')
        self.line = None
        self.line_index = 0

    def next_char(self):
        if self.line == None:
            self.line = self.input_file.readline().strip()
            if self.line == "":
                return None
            self.line_index = 0

        c = self.line[self.line_index]
        self.line_index += 1
        if self.line_index >= len(self.line):
            self.line = None
        return c

    def close(self):
        self.input_file.close()

