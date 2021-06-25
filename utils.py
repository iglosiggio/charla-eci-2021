import codecs

unicode_escape_decoder = codecs.getdecoder('unicode-escape')

def parse_string(text):
    return unicode_escape_decoder(text[1:-1])[0]

def parse_num(text):
    return float(text) if '.' in text else int(text)

class Environment:
    def __init__(self, parent=None):
        self.defs = {}
        self.parent = parent

    def lookup(self, name):
        if name in self.defs:
            return self.defs[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            raise KeyError(f'The variable {name} is not defined here')

    def store(self, name, value):
        self.defs[name] = value

    @classmethod
    def initial(cls):
        environment = cls()

        def escribir(*args):
            print(*args)
            return
        environment.store('escribir', escribir)

        def leer_num(*args):
            assert len(args) == 0
            num = input('Ingrese un número: ')
            return parse_num(num)
        environment.store('leer_num', leer_num)

        return environment
