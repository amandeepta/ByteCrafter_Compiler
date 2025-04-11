DIGITS = '0123456789'

# Token types
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

# Error class
class Error:
    def __init__(self, name, message, line, column):
        self.name = name
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return f"{self.name}: {self.message} at line {self.line + 1}, column {self.column + 1}"

# Token class
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}" if self.value is not None else self.type

# Lexer class
class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = -1
        self.current = None
        self.line = 0
        self.col = -1
        self.next()

    def next(self):
        self.index += 1
        if self.index < len(self.text):
            self.current = self.text[self.index]
            self.col += 1
            if self.current == '\n':
                self.line += 1
                self.col = -1
        else:
            self.current = None

    def make_tokens(self):
        tokens = []

        while self.current is not None:
            if self.current in ' \t':
                self.next()
            elif self.current in DIGITS:
                tokens.append(self.make_number())
            elif self.current == '+':
                tokens.append(Token(TT_PLUS)); self.next()
            elif self.current == '-':
                tokens.append(Token(TT_MINUS)); self.next()
            elif self.current == '*':
                tokens.append(Token(TT_MUL)); self.next()
            elif self.current == '/':
                tokens.append(Token(TT_DIV)); self.next()
            elif self.current == '(':
                tokens.append(Token(TT_LPAREN)); self.next()
            elif self.current == ')':
                tokens.append(Token(TT_RPAREN)); self.next()
            else:
                err = Error("IllegalCharacter", f"'{self.current}' is not valid", self.line, self.col)
                return [], err
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num = ''
        has_dot = False

        while self.current is not None and (self.current in DIGITS or self.current == '.'):
            if self.current == '.':
                if has_dot:
                    break
                has_dot = True
            num += self.current
            self.next()

        return Token(TT_FLOAT if has_dot else TT_INT, float(num) if has_dot else int(num))

# Run functio
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()


    return tokens, error

