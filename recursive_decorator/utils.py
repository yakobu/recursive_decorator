"""Utilities for recursive decorator."""
from types import CodeType, FunctionType

import sys

DECORATOR_LIST_FIELD_NAME = "__wraped_with_"


def mount_to_module(module_to_mount, object_to_mount, name_in_module):
    """Mount Given function to given module.

    Args:
        module_to_mount(module): module to mount function.
        object_to_mount(object): object to mount.
        name_in_module(str): name of object after mount to module.
    """
    setattr(module_to_mount, name_in_module, object_to_mount)


def set_func_args_and_kwargs_count(function, args_count, kwargs_count):
    """Set to given code args and kwargs count.

    Args:
        function(function): function to change.
        args_count(int): arg count to apply.
        kwargs_count(int): kwarg count to apply.
    """
    code = function.__code__
    function.__code__ = CodeType(args_count,
                                 kwargs_count,
                                 code.co_nlocals,
                                 code.co_stacksize,
                                 code.co_flags,
                                 code.co_code,
                                 code.co_consts,
                                 code.co_names,
                                 code.co_varnames,
                                 code.co_filename,
                                 code.co_name,
                                 code.co_firstlineno,
                                 code.co_lnotab,
                                 code.co_freevars,
                                 code.co_cellvars)


def get_func_module(func):
    """Return function module.

    Args:
        func(function): function to return is module.
    """
    return sys.modules[func.__module__]


def is_function(obj):
    """Return if object is function.

    Args:
        obj(object): the tested object.

    Return:
         bool. true if is function else false.
    """
    return type(obj) is FunctionType


def is_wrapped(func, decorator):
    """Return if function is already wrapped with the given decorator.

    Args:
        func(function): function to check if is wrapped.
        decorator(function): the tested decorator.

    Return:
         bool. true if is function is already wrapped else false.
    """
    if hasattr(func, DECORATOR_LIST_FIELD_NAME):
        return decorator.__name__ in getattr(func, DECORATOR_LIST_FIELD_NAME)

    return False


def get_function_wrapped_value(func):
    """Return list of decorators applied on func by recursive_decorator.

    Args:
        func(function): function to get is decorator's list.

    Return:
        list. decorators applied on func by recursive_decorator
    """
    if hasattr(func, DECORATOR_LIST_FIELD_NAME):
        return getattr(func, DECORATOR_LIST_FIELD_NAME)

    return []


def set_function_wrapped_value(func, decorator_list):
    """Set list of decorators applied by recursive_decorator.

    Args:
        func(function): function to set is decorator list.
        decorator_list(list): list of decorators applied by recursive_decorator.
    """
    setattr(func, DECORATOR_LIST_FIELD_NAME, decorator_list)
