from collections import deque
import operator
from utils import parse_num

def run_bytecode(ona_bytecode):
    i = 0
    env = {}
    stack = deque()

    def push(v):
        stack.append(v)

    def pop():
        return stack.pop()

    def is_op(opcode):
        return ona_bytecode[i] == opcode

    def binop(op):
        rhs = pop()
        lhs = pop()
        push(op(lhs, rhs))

    while i < len(ona_bytecode):
        if is_op('CONST'):
            i += 1
            push(ona_bytecode[i])
        elif is_op('LOAD'):
            push(env[pop()])
        elif is_op('STORE'):
            var = pop()
            env[var] = pop()
        elif is_op('PRINT'):
            arglist_len = pop()
            arguments = [pop() for _ in range(arglist_len)]
            arguments.reverse()
            print(*arguments)
        elif is_op('READ_NUM'):
            num = input('Ingrese un número: ')
            push(parse_num(num))
        elif is_op('JMP'):
            i = pop()
        elif is_op('JMPNT'):
            dst_i = pop()
            if not pop():
                i = dst_i
        elif is_op('ADD'):
            binop(operator.add)
        elif is_op('IS_NE'):
            binop(operator.ne)
        elif is_op('IS_GE'):
            binop(operator.ge)
        i = i + 1

    return pop() if len(stack) != 0 else None
