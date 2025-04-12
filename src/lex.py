DIGITS = '0123456789'
from src.tokenTypes import *
from src.error import *
# Position class for tracking token positions
class Position:
    def __init__(self, idx, line, col):
        self.idx = idx
        self.line = line
        self.col = col

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.line += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.line, self.col)


# Token class
class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        self.pos_start = pos_start.copy() if pos_start else None
        self.pos_end = pos_end.copy() if pos_end else None

    def __repr__(self):
        return f"{self.type}:{self.value}" if self.value is not None else self.type

# Lexer class
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, -1)
        self.current = None
        self.next()

    def next(self):
        self.pos.advance(self.current)
        if self.pos.idx < len(self.text):
            self.current = self.text[self.pos.idx]
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
                tokens.append(Token(TT_PLUS, pos_start=self.pos.copy(), pos_end=self.pos.copy())); self.next()
            elif self.current == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos.copy(), pos_end=self.pos.copy())); self.next()
            elif self.current == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos.copy(), pos_end=self.pos.copy())); self.next()
            elif self.current == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos.copy(), pos_end=self.pos.copy())); self.next()
            elif self.current == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos.copy(), pos_end=self.pos.copy())); self.next()
            elif self.current == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos.copy(), pos_end=self.pos.copy())); self.next()
            else:
                err = Error("IllegalCharacter", f"'{self.current}' is not valid", self.pos.line, self.pos.col)
                return [], err
        tokens.append(Token(TT_EOF, pos_start=self.pos.copy(), pos_end=self.pos.copy()))
        return tokens, None

    def make_number(self):
        num_str = ''
        has_dot = False
        pos_start = self.pos.copy()

        while self.current is not None and (self.current in DIGITS or self.current == '.'):
            if self.current == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += self.current
            self.next()

        value = float(num_str) if has_dot else int(num_str)
        tok_type = TT_FLOAT if has_dot else TT_INT
        return Token(tok_type, value, pos_start, self.pos.copy())

# Run function
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    return tokens, error
