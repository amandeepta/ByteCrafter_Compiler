from src.lex import run
from src.parser import Parser

text = "var a = 2+3 * (30+4)"
tokens, error = run(text)

if error:
    print(error)
else:
    print(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
