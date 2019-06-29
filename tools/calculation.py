from tools import tools
from tools import crypto

def take_degrees(dividers):
    degrees = []
    for i, num in enumerate(dividers):
        if num not in dividers[:i]:
            degrees.append(dividers.count(num)) # кол-во одинковых значение -> степень этого значения (2,2,2 -> 2^3)

    dividers = sorted(list(set(dividers))) # убираем повторяюшиеся значения

    return dividers, degrees


def replacer(string):
    replaces = {'НОД':'crypto.gcd',
                'НОК':'crypto.lcm',
                'φ':'crypto.euler',
                'F':'crypto.factorization',
                ' mod ': '%',
                '×':'*',
                '÷': '/',
                '^': '**'}

    result = string
    for text, func in replaces.items():
        result = result.replace(text, func)

    return result


def factorization_handler(fct):
    if not fct:
        return 'Простое число'

    result = ''
    dividers, degrees = take_degrees(fct)
    for divider, degree in zip(dividers, degrees):
        if degree > 1:
            result += str(divider) + '^' + str(degree) + ', '
        else:
            result += str(divider) + ', '

    if result:
        result = result[: len(result) - 2]

    return result


def mod_operations_handler(string):
    buffer = tools.junk(string)

    i = 0
    while i < len(buffer):
        if len(buffer) >= i + 3 and buffer[i] == '**' and \
                (buffer[i+2] == '%' or buffer[i+2] == ')%'):
            try:
                A = int(buffer[i - 1])
                POW = int(buffer[i + 1])
                MOD = int(buffer[i + 3])
                RESULT = crypto.bin_pow(A, POW, MOD)
            except:
                return 'Ошибка'

            buffer[i - 1] = str(RESULT)
            buffer.pop(i)
            buffer.pop(i)

        elif buffer[i] == '-¹mod ':
            try:
                E = int(buffer[i - 1])
                MOD = int(buffer[i + 1])
                RESULT = crypto.inv_mod(E, MOD)
            except:
                return 'Ошибка'

            buffer[i - 1] = str(RESULT)
            buffer[i] = '%'

        i += 1

    return ''.join([char for char in buffer])


def calculate(text):
    functions = ['crypto.euler', 'crypto.gcd',
                 'crypto.lcm', 'crypto.factorization']

    result = mod_operations_handler(replacer(text))

    END = result.find(')')
    STRT = result[: END].rfind('(')

    while '(' in result and ')' in result:

        buffer = result[STRT + 1: END]
        FUNC_BEFORE = ''
        for func in functions:
            if result[STRT - len(func): STRT] == func:
                FUNC_BEFORE = func
                break

        if '-¹mod ' in buffer or ('**' in buffer and '%' in buffer):
            buffer =  mod_operations_handler(buffer)

        try:
            if FUNC_BEFORE:
                number = buffer
                buffer = FUNC_BEFORE + '(' + buffer + ')'
                if FUNC_BEFORE == 'crypto.factorization':
                    return factorization_handler(eval(buffer))

            elif ',' in buffer:
                return 'Ошибка'

            tmp = eval(buffer)

            if crypto.isint(tmp):
                tmp = int(tmp)

            buffer = str(tmp)

        except:
            END = result[END + 1:].find(')')
            STRT = result[: STRT].rfind('(')
        else:
            result = result[:STRT - len(FUNC_BEFORE)] + buffer + result[END+1:]

            END = result.find(')')
            STRT = result[:END].rfind('(')

        if END == -1 or STRT == -1:
            break

    if '-¹mod ' in result or ('**' in result and '%' in result):
        result = mod_operations_handler(result)

    try:
        result = eval(result)
        if type(result) is float:
            if result == int(result):
                result = int(result)
    except:
        result = 'Ошибка'

    return result
