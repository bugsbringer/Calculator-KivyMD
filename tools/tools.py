from tools import crypto


def junk(string):
    result = []
    last_is_string = False
    i = 0
    while i < len(string):
        if crypto.isnum(string[i]) or (string[i] == '-'
                                and (i == 0 or string[i-1] == '(')):
            buffer = string[i]
            while i+1 < len(string) and crypto.isnum(buffer + string[i+1]):
                i += 1
                buffer += string[i]
            result.append(buffer)
            last_is_string = False
        else:
            if last_is_string:
                result[len(result)-1] += string[i]
            else:
                result.append(string[i])
                last_is_string = True
        i += 1
    return result
