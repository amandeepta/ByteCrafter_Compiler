from src.lex import run
from src.parser import Parser

from src.interpreter import Interpreter

text = "4"
tokens, error = run(text)

if error:
    print(error)
else:
    print(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
    interpreter = Interpreter()
    result = interpreter.visit(ast.node)
    print(result.value)
    print(result.error)
