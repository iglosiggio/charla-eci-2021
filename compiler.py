from antlr4 import InputStream, CommonTokenStream
from grammar.OnaVisitor import OnaVisitor
from grammar.OnaLexer import OnaLexer
from grammar.OnaParser import OnaParser
from grammar.OnaVisitor import OnaVisitor

from utils import parse_num, parse_string

class Relocation:
    def __init__(self, code):
        self._code = code
        self.value = None

    def update(self):
        self.value = len(self._code) - 1

class BytecodeCompiler(OnaVisitor):
    def __init__(self):
        self.code = []

    def label(self):
        return Relocation(self.code)

    def compile(self, parsetree):
        parsetree.accept(self)
        self.code.append('CONST')
        self.code.append(None)
        self.code.append('RET')
        return [v.value if isinstance(v, Relocation) else v for v in self.code]

    def visitStatementList(self, statement_list):
        statements = statement_list.statement()
        for statement in statements:
            statement.accept(self)

    def visitVariableAssignmentStatement(self, statement):
        varname = statement.IDENTIFIER().getText()
        statement.expression().accept(self)
        self.code.append('STORE')
        self.code.append(varname)

    def visitIfStatement(self, statement):
        else_label = self.label()
        end_if_label = self.label()

        statement.expression().accept(self)
        self.code.append('JMPNT')
        self.code.append(else_label)
        statement.then_do.accept(self)
        self.code.append('JMP')
        self.code.append(end_if_label)

        else_label.update()
        if statement.else_do is not None:
            statement.else_do.accept(self)

        end_if_label.update()

    def visitVariableReferenceExpression(self, expression):
        var_name = expression.IDENTIFIER().getText()
        self.code.append('LOAD')
        self.code.append(var_name)

    def visitNumberLiteralExpression(self, expression):
        self.code.append('CONST')
        self.code.append(parse_num(expression.NUMBER().getText()))

    def visitStringLiteralExpression(self, expression):
        self.code.append('CONST')
        self.code.append(parse_string(expression.STRING().getText()))

    def visitFunctionCall(self, function_call):
        fn_name = function_call.IDENTIFIER().getText()
        arguments = function_call.expressionList().expression()
        arity = len(arguments)

        for argument in arguments:
            argument.accept(self)

        if fn_name == 'escribir':
            self.code.append('PRINT')
            self.code.append(arity)
        elif fn_name == 'leer_num':
            assert arity == 0
            self.code.append('READ_NUM')
        else:
            raise Exception(f'{fn_name} is not a known function name')

    def visitBinaryAdditionExpression(self, expression):
        [lhs, rhs] = expression.expression()
        lhs.accept(self)
        rhs.accept(self)
        self.code.append('ADD')

    def visitGreaterThanOrEqualsExpression(self, expression):
        [lhs, rhs] = expression.expression()
        lhs.accept(self)
        rhs.accept(self)
        self.code.append('IS_GE')

    def visitNotEqualsExpression(self, expression):
        [lhs, rhs] = expression.expression()
        lhs.accept(self)
        rhs.accept(self)
        self.code.append('IS_NE')