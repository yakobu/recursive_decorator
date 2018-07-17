"""Adapter for decorator function"""


class DecoratorAdapter(object):
    """Adapter for decorator function.



    """
    def __init__(self, decorator_func, *decorator_args, **decorator_kwargs):
        self.func = decorator_func
        self.args = decorator_args
        self.kwargs = decorator_kwargs
