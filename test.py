from src.lex.lex import run
from src.Parser.parser import Parser
from src.Interpreter.interpreter import *
from src.Interpreter.context import Context
from src.Utils.symbolTable import SymbolTable


globalSymbolTable = SymbolTable()
globalSymbolTable.setv("null", Number(0))
def exec(text) :
    tokens, error = run(text)
    if error:
        print(error)
        return None
    print(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error :
        return None, ast.error
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = globalSymbolTable

    result = interpreter.visit(ast.node, context)
    return result.value, result.error


while True :
    text = input("Test-> ")
    result, error = exec(text)
    if error : print(error)
    print(result)