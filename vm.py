from collections import deque
import operator
from utils import Environment, parse_num

class BytecodedFunction:
    def __init__(self, bytecode, start, creation_env):
        self.bytecode = bytecode
        self.start = start + 1
        self.creation_env = creation_env
    def __call__(self, *args):
        return run_bytecode(self.bytecode, self.start, Environment(self.creation_env), args)

def run_bytecode(ona_bytecode, start_ip=0, env=Environment.initial(), initial_stack=()):
    i = start_ip
    stack = deque(initial_stack)

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
            push(env.lookup(arg()))
        elif is_op('STORE'):
            env.store(arg(), pop())
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
        elif is_op('CALL'):
            arglist_len = arg()
            fn = pop()
            arglist = [pop() for _ in range(arglist_len)]
            arglist.reverse()
            push(fn(*arglist))
        elif is_op('CREATE_FUNC'):
            fn_name = arg()
            fn_dst = arg()
            wrapper = BytecodedFunction(ona_bytecode, fn_dst, env)
            env.store(fn_name, wrapper)
        elif is_op('RET'):
            return pop() if len(stack) != 0 else None
        i = i + 1

    assert False

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
        if argument_list_string != '':
            argument_list_string = f'({argument_list_string})'
        print(f'{label_name}\t{offset:4X}\t{name}{argument_list_string}')

    class Label:
        def __init__(self, id):
            self.id = id

        def __repr__(self):
            return f'.label_{self.id:02}'

    last_label = 0
    label_at = {}
    i = 0

    def found_label(offset):
        nonlocal last_label
        offset += 1
        if offset not in label_at:
            label_at[offset] = Label(last_label)
            last_label += 1

    normal = lambda x: x
    label = lambda x: label_at[x + 1]

    instruction_info = {
        'CREATE_FUNC': [normal, label],
        'CONST': [normal],
        'LOAD':  [normal],
        'STORE': [normal],
        'CALL':  [normal],
        'JMP':   [label],
        'JMPNT': [label],
        'ADD':   [],
        'IS_NE': [],
        'IS_GE': [],
        'RET': [],
    }

    while i < len(ona_bytecode):
        op_name = ona_bytecode[i]
        op_argtypes = instruction_info[op_name]
        for arg_type in op_argtypes:
            arg_value = arg()
            if arg_type == label:
                found_label(arg_value)
        i = i + 1

    i = 0
    while i < len(ona_bytecode):
        op_offset = i
        op_name = ona_bytecode[i]
        op_argtypes = instruction_info[op_name]
        op_args = [argtype(arg()) for argtype in op_argtypes]
        print_instruction(op_offset, op_name, *op_args)
        i = i + 1
