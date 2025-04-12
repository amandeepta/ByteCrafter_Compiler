class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def getv(self, name):
        value = self.symbols.get(name)
        if value is None and self.parent:
            return self.parent.getv(name)
        return value

    def setv(self, name, value):
        self.symbols[name] = value
        print(f"value '{value}' is saved for '{name}'")

    def remove(self, name):
        del self.symbols[name]