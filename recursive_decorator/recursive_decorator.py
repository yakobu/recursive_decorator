"""Decorator to apply given decorator recursively on all sub functions."""
from functools import wraps

from recursive_decorator.decorator_adapter import DecoratorAdapter
from recursive_decorator.utils import mount_to_module, \
    set_func_args_and_kwargs_count, get_func_module, is_function, is_wrapped, \
    get_function_wrapped_value, set_function_wrapped_value, \
    set_function_kwargs_default_values
from .transformer import RecursiveDecoratorCallTransformer


def recursive_decorator(func_decorator, *func_decorator_args,
                        **func_decorator_kwargs):
    """Return new decorator that applying given decorator recursively
        on all sub functions."""

    @wraps(func_decorator)
    def real_decorator(func_to_decorate):
        """Decorator to apply given decorator recursively on function
            sub calls."""
        if (not is_function(func_to_decorate)) or \
                is_wrapped(func_to_decorate, func_decorator):
            return func_to_decorate

        decorator = DecoratorAdapter(func=func_decorator,
                                     args=func_decorator_args,
                                     kwargs=func_decorator_kwargs)

        func_module = get_func_module(func_to_decorate)

        mount_to_module(module_to_mount=func_module,
                        object_to_mount=recursive_decorator,
                        name_in_module=recursive_decorator.__name__)

        transformer = RecursiveDecoratorCallTransformer(func_module, decorator)
        new_func = transformer(func_to_decorate)

        # TODO: remove when
        # TODO: https://github.com/llllllllll/codetransformer/issues/67 is fixed
        old_code = func_to_decorate.__code__
        set_func_args_and_kwargs_count(new_func,
                                       old_code.co_argcount,
                                       old_code.co_kwonlyargcount)

        # TODO: remove when
        # TODO: https://github.com/llllllllll/codetransformer/issues/69 is fixed
        set_function_kwargs_default_values(new_func,
                                           func_to_decorate.__kwdefaults__)

        already_wrapped_dec = get_function_wrapped_value(func_to_decorate)[:]
        wrapped_function_list = already_wrapped_dec + [func_decorator.__name__]

        value = decorator.wrapper(new_func)
        if is_function(value):
            set_function_wrapped_value(value, wrapped_function_list)

        return value

    return real_decorator
