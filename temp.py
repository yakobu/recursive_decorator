from recursive_decorator import recursive_decorator
import dis
from inspect import getsourcelines


def dec1(f):
    print("dec1")
    return f


def dec2(f):
    print("dec2")
    return f


def g():
    print("Enter to g")


def f():
    g()


gg = recursive_decorator(dec1)(f)
ee = recursive_decorator(dec2)(gg)


def q():
    getsourcelines(f)

qq = recursive_decorator(dec2)(recursive_decorator(dec1)(q))
