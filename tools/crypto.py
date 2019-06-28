import math
from tools.factorization import factor, miller_rabin

def bin_pow(a, deg, mod):
    if (type(a), type(deg), type(mod)) is (int, int, int):
         #Более быстрый алгоритм, но работает только с целыми
        return pow(a, deg, mod)

    # а мой позволяет работать с нецелыми числами (кроме степени)
    Ai = a
    for i in bin(deg)[3:]:
        Ai = Ai**2 * a**int(i) % mod
    return Ai


def factorization(N):
    # привычная обертка
    dividers = factor(N)
    if dividers[0] == N: # при N простом возвращает [N]
        dividers = [] # удобно для зависямых функций, если N простое -> []

    return dividers


def euler(n):
    if n > 1:
        dividers = set(factorization(n)) #исключаем повторения
        if not dividers:
            return n - 1
        else:
            buf = 1
            for divider in dividers:
                buf *= 1 - 1 / divider
            return round(n * buf)
    elif n == 1:
        return 1
    else:
        return None


def primitive_root(g, mod):
    euler_function = euler(mod)

    if g >= euler_function:
        return False, tuple()

    dividers = set(factorization(euler_function))#исключаем повторения

    results = []
    for divider in dividers:
        result = pow(g, euler_function / divider, mod)
        results.append(result)

        if result == 1:
            return False, tuple([euler_function,dividers,results])

    return True, tuple([euler_function,dividers,results])


def gcd(*args):
    """НОД, Попарная проверка"""
    if len(args) < 2:
        raise TypeError('gcd() takes exactly 2 or more arguments(%s given)' % len(args))

    elif 0 in args:
        raise ValueError('arguments should not be zero')

    else:
        result = math.gcd(abs(args[0]), abs(args[1]))

        if len(args) > 2:

            for arg in args[2:]:
                result = math.gcd(result, arg)

        return result


def lcm(*args):
    """НОК"""
    if len(args) > 1:
        a, b = abs(args[0]), abs(args[1])
        result = a * b // math.gcd(a, b)

        if len(args) > 2:
            for b in args[2:]:
                result = lcm(result, b)

        return result
    else:
        raise TypeError('lcm takes exactly 2 or more arguments(%s given)' % len(args))


def inv_mod(e, mod):

    return pow(e, euler(mod) - 1, mod)


def ceil(n):
    """округеление n к большему"""
    if int(n) != n:
        n = int(n) + 1
    return int(n)


def isdigit(n):
    try:
        n = float(n)
    except Exception as e:
        return False
    else:
        if n == int(n):
            return True
        else:
            return False


def isnum(n):
    '''можно ли перевести n(строку и тп.) в число'''
    try:
        n = float(n)
    except Exception as e:
        return False
    else:
        return True


def isint(n):
    try:
        int(n)
    except Exception as e:
        return False
    else:
        if n == int(n):
            return True
        else:
            return False


def isprime(n):
    if n > 1 and not factorization(n):
        return True
    else:
        return False
