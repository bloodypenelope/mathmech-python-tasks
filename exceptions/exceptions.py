import sys


def f0():
    sys.exit(1)


def f1():
    assert 1 != 1


def f2():
    a = 0 / 0


def f3():
    raise FloatingPointError
    # no longer used


def f4():
    a = 2.0
    for i in range(1, 1000):
        a = a ** i


def f5():
    a = 0 / 0


def f6():
    assert 1 == 0


def f7():
    a = list()
    a.dasdasd


def f8():
    file = open('abracadabra.txt', 'r')


def f9():
    import asdfg


def f10():
    a = {
        '1': 1,
        '2': 2,
    }
    a['3']


def f11():
    a = [1]
    b = a[1]


def f12():
    a = {
        '1': 1,
        '2': 2,
    }
    a['3']


def f13():
    принт('Hello World!')


def f14():
    eval('one times one')


def f15():
    chr(-1)


def f16():
    'привет'.encode('ascii')


def check_exception(f, exception):
    try:
        f()
    except exception:
        pass
    else:
        print("Bad luck, no exception caught: %s" % exception)
        sys.exit(1)


check_exception(f0, BaseException)
check_exception(f1, Exception)
check_exception(f2, ArithmeticError)
check_exception(f3, FloatingPointError)
check_exception(f4, OverflowError)
check_exception(f5, ZeroDivisionError)
check_exception(f6, AssertionError)
check_exception(f7, AttributeError)
check_exception(f8, EnvironmentError)
check_exception(f9, ImportError)
check_exception(f10, LookupError)
check_exception(f11, IndexError)
check_exception(f12, KeyError)
check_exception(f13, NameError)
check_exception(f14, SyntaxError)
check_exception(f15, ValueError)
check_exception(f16, UnicodeError)

print("Congratulations, you made it!")
