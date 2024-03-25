def long_division(dividend, divider):
    """
    Вернуть строку с процедурой деления «уголком» чисел dividend и divider.
    Формат вывода приведён на примерах ниже.

    Примеры:
    >>> 12345÷25
    12345|25
    100  |493
     234
     225
       95
       75
       20

    >>> 1234÷1423
    1234|1423
    1234|0

    >>> 24600÷123
    24600|123
    246  |200
      0

    >>> 246001÷123
    246001|123
    246   |2000
         1
    """

    digits = list(map(int, str(dividend)))
    output = list()
    output.append(f"{dividend}|{divider}")
    rem = offset = result = 0
    while digits:
        rem = rem * 10 + digits.pop(0)
        if rem >= divider:
            if offset:
                output.append(f"{'':<{offset}}{rem}")
            rem_len = len(str(rem))
            res, rem = divmod(rem, divider)
            result = result * 10 + res
            output.append(f"{'':<{offset}}{res * divider:>{rem_len}}")
            offset += rem_len - len(str(rem)) + (0 if rem else 1)
        else:
            result *= 10
    if rem:
        output.append(f"{' ' * (len(str(dividend)) - len(str(rem)))}{rem}")
    else:
        output.append(f"{'':<{offset - 1}}{rem}")
    output[1] += ' ' * (len(str(dividend)) - len(output[1])) + f'|{result}'
    return '\n'.join(output)


def main():
    print(long_division(123, 123))
    print()
    print(long_division(1, 1))
    print()
    print(long_division(15, 3))
    print()
    print(long_division(3, 15))
    print()
    print(long_division(12345, 25))
    print()
    print(long_division(1234, 1423))
    print()
    print(long_division(87654532, 1))
    print()
    print(long_division(24600, 123))
    print()
    print(long_division(4567, 1234567))
    print()
    print(long_division(246001, 123))
    print()
    print(long_division(100000, 50))
    print()
    print(long_division(123456789, 531))
    print()
    print(long_division(425934261694251, 12345678))


if __name__ == '__main__':
    main()
