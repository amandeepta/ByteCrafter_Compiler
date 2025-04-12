from .tokens import *
from .error import Error

import string


DIGITS = '0123456789'
LETTERS = string.ascii_letters  #for strict ascii controls
LETTERS_DIGITS = LETTERS + DIGITS

# Lexer class
class Lexer:
    def __init__(self, text):
        self.text = text
        self.index = Position(-1, 0, 1)
        self.current = None
        self.next()

    def next(self):
        self.index.advance(self.current)

        if self.index.idx < len(self.text):
            self.current = self.text[self.index.idx]
        else:
            self.current = None

    def make_tokens(self):
        tokens = []

        while self.current is not None:
            # skip blank spaces
            if self.current in ' \t':
                self.next()

            # numeric values
            elif self.current in DIGITS:
                tokens.append(self.make_number())

            # identifier/keywords
            elif self.current in LETTERS:
                tokens.append(self.make_identifiers())

            # binary operators
            elif self.current == '+':
                tokens.append(self.make_simple_token(TT_PLUS))
            elif self.current == '-':
                tokens.append(self.make_simple_token(TT_MINUS))
            elif self.current == '*':
                tokens.append(self.make_simple_token(TT_MUL))
            elif self.current == '/':
                tokens.append(self.make_simple_token(TT_DIV))

            # parenthesis
            elif self.current == '(':
                tokens.append(self.make_simple_token(TT_LPAREN))
            elif self.current == ')':
                tokens.append(self.make_simple_token(TT_RPAREN))

            # equality
            elif self.current == '=':
                token, error = self.make_equals(TT_EQ)
                if error: return [], error
                tokens.append(token)

            elif self.current == '!':
                token, error = self.make_not_equals()
                if error: return [], error
                tokens.append(token)

            elif self.current == '<':
                token, error = self.make_less_than()
                if error: return [], error
                tokens.append(token)

            elif self.current == '>':
                token, error = self.make_greater_than()
                if error: return [], error
                tokens.append(token)

            else:
                err = Error("IllegalCharacter", f"'{self.current}' is not valid", self.index.line, self.index.col)
                return [], err

        tokens.append(Token(TT_EOF))
        return tokens, None

    def make_simple_token(self, type_):
        pos_start = self.index.copy()
        self.next()
        return Token(type_, pos_start=pos_start, pos_end=self.index.copy())

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

    def make_identifiers(self):
        id_str = ""
        pos_start = self.index.copy()

        while self.current is not None and self.current in LETTERS_DIGITS + '-':
            id_str += self.current
            self.next()
        
        if id_str.upper() in KEYWORDS:
            token_type = TT_KEYWORD
            id_str = id_str.upper()  
        else:
            token_type = TT_IDENTIFIER
        
        return Token(token_type, id_str, pos_start, self.index.copy())


    def make_not_equals(self):
        pos_start = self.index.copy()
        self.next()

        if self.current == '=':
            self.next()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.index.copy()), None
        else:
            return None, Error("IllegalCharacter", "'=' expected after '!'", self.index.line, self.index.col)

    def make_equals(self, type_):
        pos_start = self.index.copy()
        self.next()

        if self.current == '=':
            self.next()
            return Token(TT_EE, pos_start=pos_start, pos_end=self.index.copy()), None
        else:
            return Token(type_, pos_start=pos_start, pos_end=self.index.copy()), None

    def make_less_than(self):
        pos_start = self.index.copy()
        self.next()

        if self.current == '=':
            self.next()
            return Token(TT_LTE, pos_start=pos_start, pos_end=self.index.copy()), None
        else:
            return Token(TT_LT, pos_start=pos_start, pos_end=self.index.copy()), None

    def make_greater_than(self):
        pos_start = self.index.copy()
        self.next()

        if self.current == '=':
            self.next()
            return Token(TT_GTE, pos_start=pos_start, pos_end=self.index.copy()), None
        else:
            return Token(TT_GT, pos_start=pos_start, pos_end=self.index.copy()), None

# Run function
def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    return tokens, error

def main():
    text = "var a = 2 + 3 * (30 + 4)"
    tokens, error = run(text)

    if error:
        print(error)
    else:
        print(tokens)

if __name__ == "__main__":
    main()
