import codecs
from grammar.OnaVisitor import OnaVisitor

unicode_escape_decoder = codecs.getdecoder('unicode-escape')

def unescape(text):
    return unicode_escape_decoder(text)[0]

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

class Interpreter(OnaVisitor):
    def __init__(self, environment):
        self.environment = environment

    def run(self, code):
        return code.accept(self)

    def parse_num(self, number):
        text = number.getText()
        return parse_num(text)

    def parse_string(self, string):
        text = string.getText()[1:-1] # Trim start and end quotes
        return unescape(text)

    def visitStatementList(self, statement_list):
        statements = statement_list.statement()
        last_result = None

        for statement in statements:
            last_result = statement.accept(self)

        return last_result

    def visitVariableAssignmentStatement(self, statement):
        var_name = statement.IDENTIFIER().getText()
        var_value = statement.expression().accept(self)
        self.environment.store(var_name, var_value)
        return var_value

    def visitIfStatement(self, statement):
        guard = statement.expression()
        then_do = statement.then_do
        else_do = statement.else_do

        condition_value = guard.accept(self)

        if condition_value:
            return then_do.accept(self)
        elif else_do is not None:
            return else_do.accept(self)

        return None

    def visitVariableExpression(self, expression):
        var_name = expression.IDENTIFIER().getText()
        return self.environment.lookup(var_name)

    def visitNumberLiteralExpression(self, expression):
        return self.parse_num(expression.NUMBER())

    def visitStringLiteralExpression(self, expression):
        return self.parse_string(expression.STRING())

    def visitBinaryAdditionExpression(self, expression):
        [lhs, rhs] = expression.expression()
        lhs_value = lhs.accept(self)
        rhs_value = rhs.accept(self)
        return lhs_value + rhs_value

    def visitGreatherThanExpression(self, expression):
        [lhs, rhs] = expression.expression()
        lhs_value = lhs.accept(self)
        rhs_value = rhs.accept(self)
        return lhs_value >= rhs_value

    def visitNotEqualsExpression(self, expression):
        [lhs, rhs] = expression.expression()
        lhs_value = lhs.accept(self)
        rhs_value = rhs.accept(self)
        return lhs_value != rhs_value

    def visitFunctionCall(self, call):
        fn_name = call.IDENTIFIER().getText()

        if fn_name == 'escribir':
            print(*[
                expression.accept(self)
                for expression in call.expressionList().expression()
            ])
            return
        elif fn_name == 'leer_num':
            num = input('Ingrese un número: ')
            return parse_num(num)

        raise Exception(f'{fn_name} is not a known function name')
