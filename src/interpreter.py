#######################################
# TOKEN TYPES
#######################################
TT_INT      = 'INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_EOF      = 'EOF'
#creates a interpreter to solve the ast node 
class Interpreter: 
    #this method will return the token value of 
    def visit(self, node):
        #creates the method name to call from the given node
        method_name = f'visit_{type(node).__name__}'
        #if method_name exist then use method_name else use self.no_visit_method
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    #creates the error if no type of the node exists
    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    #returns the number token value
    def visit_NumberNode(self, node):
        print("Found the NumberNode")
        return Number(node.tok.value).set_pos(node.pos_start, node.pos_end)

    #perform the binary operation
    def visit_BinOpNode(self, node): 
        print("Found the BinOpNode")
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if node.op_tok.type == TT_PLUS:
            return left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            return left.sub_by(right)
        elif node.op_tok.type == TT_MUL:
            return left.mul_to(right)
        elif node.op_tok.type == TT_DIV:
            return left.div_by(right)

        raise Exception(f"Unknown operator {node.op_tok.type}") 

    def visit_UnaryOpNode(self, node):
        print("op found")
        number = self.visit(node.node)

        if node.op_tok.type == TT_MINUS:
            return Number(-number.value).set_pos(node.pos_start, node.pos_end)
        elif node.op_tok.type == TT_PLUS:
            return number

        raise Exception(f"Unknown unary operator {node.op_tok.type}")


# Number class to wrap values
class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self  # allows chaining like Number(...).set_pos(...)

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

    def sub_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)

    def mul_to(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    def div_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                raise Exception("Division by zero")
            return Number(self.value / other.value)

    def __repr__(self):
        return str(self.value)


