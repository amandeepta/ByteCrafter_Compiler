from src.lex import run

text = "2+3"
tokens, error = run(text)

if error:
    print(error)
else:
    print(tokens)
