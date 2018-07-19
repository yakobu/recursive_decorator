"""Decorator to apply given decorator recursively on all sub functions."""
import sys
from functools import wraps
from types import CodeType, FunctionType

from recursive_decorator.decorator_adapter import DecoratorAdapter
from recursive_decorator.utils import mount_function_to_module
from .transformer import RecursiveDecoratorCallTransformer


def recursive_decorator(func_decorator, *func_decorator_args,
                        **func_decorator_kwargs):
    """Apply given decorator recursively on all sub functions."""

    @wraps(func_decorator)
    def real_decorator(func_to_decorate):
        """"""
        if type(func_to_decorate) is not FunctionType:
            return func_to_decorate

        if hasattr(func_to_decorate, "__wraped_with_"):
            if func_decorator.__name__ in func_to_decorate.__wraped_with_:
                return func_to_decorate

        decorator = DecoratorAdapter(func=func_decorator,
                                     args=func_decorator_args,
                                     kwargs=func_decorator_kwargs)

        func_module = sys.modules[func_to_decorate.__module__]

        mount_function_to_module(func_module, recursive_decorator)
        mount_function_to_module(func_module, func_decorator)

        decorator_args_name = \
            func_decorator.__name__ + "_" + recursive_decorator.__name__ + "_args"
        setattr(func_module, decorator_args_name, func_decorator_args)

        decorator_kwargs_name = \
            func_decorator.__name__ + "_" + recursive_decorator.__name__ + "_kwargs"
        setattr(func_module, decorator_kwargs_name, func_decorator_kwargs)

        call_transformer = \
            RecursiveDecoratorCallTransformer(func_decorator.__name__,
                                              decorator_args_name,
                                              decorator_kwargs_name)
        new_func = call_transformer(func_to_decorate)

        occ = func_to_decorate.__code__
        ncc = new_func.__code__
        zz = CodeType(occ.co_argcount,
                      occ.co_kwonlyargcount,
                      ncc.co_nlocals,
                      ncc.co_stacksize,
                      ncc.co_flags,
                      ncc.co_code,
                      ncc.co_consts,
                      ncc.co_names,
                      ncc.co_varnames,
                      ncc.co_filename,
                      ncc.co_name,
                      ncc.co_firstlineno,
                      ncc.co_lnotab,
                      ncc.co_freevars,
                      ncc.co_cellvars)

        new_func.__code__ = zz

        if hasattr(func_to_decorate, "__wraped_with_"):
            new_func.__wraped_with_ = func_to_decorate.__wraped_with_[:]
        else:
            new_func.__wraped_with_ = []

        new_func.__wraped_with_.append(func_decorator.__name__)

        return decorator.wrapper(new_func)

    return real_decorator
