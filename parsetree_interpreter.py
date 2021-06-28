from grammar.OnaVisitor import OnaVisitor
from utils import Environment, parse_num, parse_string

class Interpreter(OnaVisitor):
    def __init__(self):
        self.environment = Environment.initial()

    def run(self, code):
        return code.accept(self)

    def parse_num(self, number):
        text = number.getText()
        return parse_num(text)

    def parse_string(self, string):
        text = string.getText()
        return parse_string(text)

    def visitStatementList(self, statement_list):
        statements = statement_list.statement()
        last_result = None

        for statement in statements:
            last_result = statement.accept(self)
            if statement.returnStatement() is not None:
                return last_result

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

    def visitFunctionDefinitionStatement(self, statement):
        fn_name = statement.IDENTIFIER().getText()
        argument_names = [arg.getText() for arg in statement.argumentList().IDENTIFIER()]
        fn_body = statement.statementList()

        creation_end = self.environment
        def wrapper(*args):
            callee_env = self.environment
            self.environment = Environment(creation_end)
            for i, arg in enumerate(argument_names):
                self.environment.store(arg, args[i])
            result = fn_body.accept(self)
            self.environment = callee_env
            return result

        self.environment.store(fn_name, wrapper)

    def visitVariableReferenceExpression(self, expression):
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

    def visitGreaterThanOrEqualsExpression(self, expression):
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
        args = [
            expression.accept(self)
            for expression in call.expressionList().expression()
        ]
        fn = self.environment.lookup(fn_name)
        return fn(*args)
