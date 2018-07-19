"""Adapter for decorator function"""
from cached_property import cached_property


class DecoratorAdapter(object):
    """Adapter for decorator function.

    Attributes:
        func(func): the decorator function.
        decorator_args(tuple): the decorator args.
        decorator_kwargs(dict): the decorator kwargs.
    """
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    @cached_property
    def wrapper(self):
        """Get real decorator function after args injection if needed.

        Return:
            function. wrapper if has args or kwargs, else the decorator itself.
        """
        if self.args or self.kwargs:
            return self.func(*self.args,**self.kwargs)

        return self.func
