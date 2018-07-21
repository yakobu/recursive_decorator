"""Call transformer module."""
from codetransformer import CodeTransformer, pattern
from codetransformer.instructions import (CALL_FUNCTION, BUILD_TUPLE, ROT_TWO,
                                          LOAD_GLOBAL, UNPACK_SEQUENCE,
                                          CALL_FUNCTION_VAR_KW,
                                          CALL_FUNCTION_VAR,
                                          CALL_FUNCTION_KW)

from recursive_decorator.utils import mount_to_module


class RecursiveDecoratorCallTransformer(CodeTransformer):
    """Transformer class for every call in function.

    Arguments:
        function_module(module): module of function to transform.
        decorator(DecoratorAdapter): adapter of decorator to apply on sub calls.

    """
    CALL_TYPES = CALL_FUNCTION | CALL_FUNCTION_VAR | CALL_FUNCTION_KW | \
                 CALL_FUNCTION_VAR_KW

    RECURSIVE_DECORATOR = "recursive_decorator"

    def __init__(self, function_module, decorator):
        self.decorator_adapter_name = decorator.adapter_name
        mount_to_module(module_to_mount=function_module,
                        object_to_mount=tuple(reversed(decorator.as_tuple)),
                        name_in_module=self.decorator_adapter_name)

    @pattern(LOAD_GLOBAL[2], UNPACK_SEQUENCE, CALL_FUNCTION_VAR_KW, ROT_TWO,
             CALL_FUNCTION,
             ROT_TWO, UNPACK_SEQUENCE, BUILD_TUPLE, UNPACK_SEQUENCE,
             CALL_TYPES)
    def _call(self, g1, *ins):
        yield g1
        yield from ins[:5]
        if g1.arg == "recursive_decorator":
            yield from self.wrap_function_with_recursive_decorator()
        yield from ins[5:]

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
        """switch function and args stack position.

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
        """Switch args and function stack position.

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
        yield LOAD_GLOBAL(self.decorator_adapter_name)
        yield UNPACK_SEQUENCE(3)
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
