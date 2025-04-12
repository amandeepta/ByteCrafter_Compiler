from src.Utils.tokens import *
from src.Utils.error import *
from src.Utils.symbolTable import *
from src.Interpreter.context import *

#######################################
# Number Class
#######################################

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def sub_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def mul_to(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def div_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end, 'Division by zero', self.context)
            return Number(self.value / other.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)

#######################################
# RTResult Class
#######################################

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

#######################################
# Interpreter Class
#######################################

class Interpreter:
    def visit(self, node, context):
        res = RTResult()
        if node is None:
            return res.failure(RTError(None, None, 'Tried to interpret a None node — possibly a parser error.', context))
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node, context):
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.getv(var_name)
        if value is None:
            return res.failure(RTError(node.pos_start, node.pos_end, f'{var_name} is not defined', context))
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res
        var_name = node.var_name_tok.value
        context.symbol_table.setv(var_name, value)
        return res.success(value.set_pos(node.pos_start, node.pos_end))

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.sub_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.mul_to(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.div_by(right)
        else:
            return res.failure(RTError(node.pos_start, node.pos_end, 'Unknown binary operator', context))

        if error:
            return res.failure(error)
        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None
        if node.op_tok.type == TT_MINUS:
            number, error = number.mul_to(Number(-1).set_context(context))

        if error:
            return res.failure(error)
        return res.success(number.set_pos(node.pos_start, node.pos_end))
