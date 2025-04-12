from src.Utils.tokens import *
from src.Utils.error import *
from src.Parser.nodes import *
#######################################
# PARSE RESULT
#######################################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

    def __repr__(self):
        return f'Error: {self.error}' if self.error else f'Node: {self.node}'

#######################################
# PARSER
#######################################
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok = None
        self.advance()

    def __repr__(self):
        return f'Parser: {self.tokens}'

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                getattr(self.current_tok, 'pos_start', None),
                getattr(self.current_tok, 'pos_end', None),
                "Expected '+', '-', '*', or '/'"
            ))
        return res

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            op_tok = tok
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, factor))

        elif tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_IDENTIFIER:
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    getattr(self.current_tok, 'pos_start', None),
                    getattr(self.current_tok, 'pos_end', None),
                    "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError(
            getattr(tok, 'pos_start', None),
            getattr(tok, 'pos_end', None),
            "Expected int, float, '+', '-', or '('"
        ))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register(self.advance())

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected identifier"
                ))
            
            var_name = self.current_tok
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected '='"
                ))

            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))
                        

        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_tok is not None and self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
