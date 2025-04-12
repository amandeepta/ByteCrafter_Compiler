from src.Utils.tokens import *
from src.Utils.error import *


#######################################
# Number Class

#######################################
'''
 bhai is number class ko bhi utils m shift krna??
'''
class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value), None

    def sub_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value), None

    def mul_to(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value), None

    def div_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end, 'Division by zero')
            return Number(self.value / other.value), None

    def __repr__(self):
        return str(self.value)


#######################################
# RTResult Class
#######################################
'''
aur yeh bhi???
'''
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
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node):
        print("Found the NumberNode")
        return RTResult().success(Number(node.tok.value).set_pos(node.pos_start, node.pos_end))
    
    def visit_VarAssignNode(self, node):
        print("Found the VarAssignNode")
        res = RTResult()
        value = res.register(self.visit(node.value_node))
        if res.error: return res
        var_name = node.var_name_tok.value
        # Assuming we have a context to store variables
        # context.set(var_name, value)
        return res.success(value.set_pos(node.pos_start, node.pos_end))

    def visit_BinOpNode(self, node):
        print("Found the BinOpNode")
        res = RTResult()
        left = res.register(self.visit(node.left_node))
        if res.error: return res
        right = res.register(self.visit(node.right_node))
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
            return res.failure(RTError(node.pos_start, node.pos_end, 'Unknown binary operator'))

        if error:
            return res.failure(error)
        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node):
        print("Found UnaryOpNode")
        res = RTResult()
        number = res.register(self.visit(node.node))
        if res.error: return res

        error = None
        if node.op_tok.type == TT_MINUS:
            number, error = number.mul_to(Number(-1))

        if error:
            return res.failure(error)
        return res.success(number.set_pos(node.pos_start, node.pos_end))
