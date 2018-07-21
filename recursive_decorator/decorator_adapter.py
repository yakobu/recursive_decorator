"""Adapter for decorator function"""
from cached_property import cached_property


class DecoratorAdapter(object):
    """Adapter for decorator function.

    Attributes:
        func(func): the decorator function.
        args(tuple): the decorator args.
        kwargs(dict): the decorator kwargs.
    """
    ADAPTER_NAME_PATTERN = "{decorator_name}_adapter"

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
            return self.func(*self.args, **self.kwargs)

        return self.func

    @property
    def adapter_name(self):
        """Decorator adapter name."""
        decorator_name = self.func.__name__
        return self.ADAPTER_NAME_PATTERN.format(decorator_name=decorator_name)

    @property
    def as_tuple(self):
        """Return decorator fields as tuple.

        Return:
            tuple. decorator, args, kwargs
        """
        return self.func, self.args, self.kwargs
