from src.position import Position

# Token types
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EQ = 'EQ'
TT_EE = 'EE'
TT_NE = 'NE'
TT_GT = 'GT'
TT_LT = 'LT'
TT_GTE = 'GTE'
TT_LTE = 'LTE'
TT_EOF = 'EOF'

#keywords
KEYWORDS = [
    'VAR', 
    'CONST',
    'INT',
    'FLOAT',
    'AND',
    'OR',
    'NOT',
]


# Token class
class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        self.pos_start = pos_start.copy() if pos_start else None
        self.pos_end = pos_end.copy() if pos_end else None

        if pos_start and not pos_end:
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

    def __repr__(self):
        return f"{self.type}:{self.value}" if self.value is not None else self.type

    def matches(self, type, value):
        return self.type == type and self.value == value
    

