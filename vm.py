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

    def arg():
        nonlocal i
        i += 1
        return ona_bytecode[i]

    while i < len(ona_bytecode):
        if is_op('CONST'):
            push(arg())
        elif is_op('LOAD'):
            push(env[arg()])
        elif is_op('STORE'):
            env[arg()] = pop()
        elif is_op('PRINT'):
            arglist_len = arg()
            arguments = [pop() for _ in range(arglist_len)]
            arguments.reverse()
            print(*arguments)
        elif is_op('READ_NUM'):
            num = input('Ingrese un número: ')
            push(parse_num(num))
        elif is_op('JMP'):
            i = arg()
        elif is_op('JMPNT'):
            dst_i = arg()
            if not pop():
                i = dst_i
        elif is_op('ADD'):
            binop(operator.add)
        elif is_op('IS_NE'):
            binop(operator.ne)
        elif is_op('IS_GE'):
            binop(operator.ge)
        elif is_op('RET'):
            return pop()
        i = i + 1

    return pop() if len(stack) != 0 else None

def print_bytecode(ona_bytecode):

    def is_op(opcode):
        return ona_bytecode[i] == opcode

    def arg():
        nonlocal i
        i += 1
        return ona_bytecode[i]
    
    def print_instruction(offset, name, *args):
        label_name = label_at.get(offset, '         ')
        argument_list_string = ', '.join(repr(arg) for arg in args)
        print(f'{label_name}\t{offset:4X}\t{name}({argument_list_string})')


    class Label:
        def __init__(self, id):
            self.id = id

        def __repr__(self):
            return f'.label_{self.id:02}'

    last_label = 0
    label_at = {}
    i = 0
    while i < len(ona_bytecode):
        if is_op('CONST') or is_op('LOAD') or is_op('STORE') or is_op('PRINT'):
            # Skip argument
            arg()
        elif is_op('JMP') or is_op('JMPNT'):
            dst = arg() + 1
            if dst not in label_at:
                label_at[dst] = Label(last_label)
                last_label += 1
        i = i + 1

    i = 0
    while i < len(ona_bytecode):
        if is_op('CONST'):
            print_instruction(i, 'CONST', arg())
        elif is_op('LOAD'):
            print_instruction(i, 'LOAD', arg())
        elif is_op('STORE'):
            print_instruction(i, 'STORE', arg())
        elif is_op('PRINT'):
            print_instruction(i, 'PRINT', arg())
        elif is_op('READ_NUM'):
            print_instruction(i, 'READ_NUM')
        elif is_op('JMP'):
            dst = label_at[arg() + 1]
            print_instruction(i, 'JMP', dst)
        elif is_op('JMPNT'):
            dst = label_at[arg() + 1]
            print_instruction(i, 'JMPNT', dst)
        elif is_op('ADD'):
            print_instruction(i, 'ADD')
        elif is_op('IS_NE'):
            print_instruction(i, 'IS_NE')
        elif is_op('IS_GE'):
            print_instruction(i, 'IS_GE')
        elif is_op('RET'):
            print_instruction(i, 'RET')
        i = i + 1
