"""Call transformer module."""
from codetransformer import CodeTransformer, pattern
from codetransformer.instructions import (CALL_FUNCTION, BUILD_TUPLE, ROT_TWO,
                                          LOAD_GLOBAL, UNPACK_SEQUENCE,
                                          CALL_FUNCTION_VAR_KW,
                                          CALL_FUNCTION_VAR,
                                          CALL_FUNCTION_KW)


class RecursiveDecoratorCallTransformer(CodeTransformer):
    """Transformer class for every call in function."""
    CALL_TYPES = CALL_FUNCTION | CALL_FUNCTION_VAR | CALL_FUNCTION_KW |\
                 CALL_FUNCTION_VAR_KW

    def __init__(self, decorator_name, decorator_args_name,
                 decorator_kwargs_name):
        self.decorator_name = decorator_name
        self.decorator_args_name = decorator_args_name
        self.decorator_kwargs_name = decorator_kwargs_name

    RECURSIVE_DECORATOR = "recursive_decorator"

    @pattern(CALL_TYPES)
    def _call_transformer(self, call):
        """Transformer to wrap calls with recursive_decorator"""
        call_args_count = self.call_params_count(call)

        yield from self.switch_function_and_args(call_args_count)
        yield from self.wrap_function_with_recursive_decorator()
        yield from self.switch_args_and_function(call_args_count)
        yield call

    @staticmethod
    def call_params_count(call):
        """Calculate function call number of arguments.

        Return:
             int. function call number of arguments.
        """
        call_args_count = call.positional + 2 * call.keyword
        if type(call) in (CALL_FUNCTION_VAR, CALL_FUNCTION_KW):
            call_args_count += 1

        elif type(call) is CALL_FUNCTION_VAR_KW:
            call_args_count += 2
        return call_args_count

    @staticmethod
    def switch_function_and_args(args_count):
        """

        Arguments:
            args_count(int): number of arguments supplied to function call.

        Yield:
            instructions to switch order in stack of call function and args,
        """
        # Make tuple of all function args
        yield BUILD_TUPLE(args_count)
        # Switch between function and args
        yield ROT_TWO()

    @staticmethod
    def switch_args_and_function(args_count):
        """

        Arguments:
            args_count(int): number of arguments supplied to function call.

        Yield:
            instructions to switch order in stack of call function and args,
        """
        # Switch function and tuple of args
        yield ROT_TWO()
        # Unpack args in the same order they supplied
        yield UNPACK_SEQUENCE(args_count)
        yield BUILD_TUPLE(args_count)
        yield UNPACK_SEQUENCE(args_count)

    def apply_recursive_decorator_on_decorator(self):
        """Call recursive_decorator(decorator, *args, **kwargs).

        Yield:
            instructions to apply recursive_decorator on decorator.
        """
        yield LOAD_GLOBAL(self.RECURSIVE_DECORATOR)
        yield LOAD_GLOBAL(self.decorator_name)
        yield LOAD_GLOBAL(self.decorator_args_name)
        yield LOAD_GLOBAL(self.decorator_kwargs_name)
        yield CALL_FUNCTION_VAR_KW(1)

    def wrap_function_with_recursive_decorator(self):
        """Wrap function with recursive_decorator.

        Yield:
             instructions to wrap function with recursive_decorator.
        """
        yield from self.apply_recursive_decorator_on_decorator()

        # Apply recursive_decorator(dec) on function
        yield ROT_TWO()
        yield CALL_FUNCTION(1)
