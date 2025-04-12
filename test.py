from src.lex.lex import run
from src.Parser.parser import Parser
from src.Interpreter.interpreter import Interpreter

text = "var 12a =2+3"
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
