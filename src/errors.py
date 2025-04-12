# Error class
class Error:
    def __init__(self, name, message, line, column):
        self.name = name
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return f"{self.name}: {self.message} at line {self.line + 1}, column {self.column + 1}"


class InvalidSyntaxError(Exception):
    def __init__(self, pos_start, pos_end, message):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.message = message

    def __str__(self):
        return f"Invalid Syntax Error: {self.message}"