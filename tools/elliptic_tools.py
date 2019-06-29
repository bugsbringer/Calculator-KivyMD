from tools import crypto
from tools import tools
from tools.elliptic import EllipticCurve, Point

def calculate(string, curve):
    string = string.replace('(', 'Point(curve,')
    try:
        result = eval(string)
    except:
        return False
    else:
        return result

def parse_curve_data(curve_data):
    data = tools.junk(curve_data)

    if len(data) != 6 or (data[1], data[3], data[5]) != ('(', ',', ')'):
        return False

    if any([not crypto.isdigit(data[i]) for i in (0,2,4)]):
        return False

    p = int(data[0])
    a = int(data[2])
    b = int(data[4])

    return EllipticCurve((a, b), p)
