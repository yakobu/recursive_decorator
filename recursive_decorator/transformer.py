"""Call transformer module."""
from codetransformer import CodeTransformer, pattern
from codetransformer.instructions import (CALL_FUNCTION, BUILD_TUPLE, ROT_TWO,
                                          LOAD_GLOBAL, UNPACK_SEQUENCE,
                                          CALL_FUNCTION_VAR_KW,
                                          CALL_FUNCTION_VAR,
                                          CALL_FUNCTION_KW)


class RecursiveDecoratorCallTransformer(CodeTransformer):
    """Transformer class for every call in function."""

    def __init__(self, decorator_name, decorator_args_name,
                 decorator_kwargs_name):
        self.decorator_name = decorator_name
        self.decorator_args_name = decorator_args_name
        self.decorator_kwargs_name = decorator_kwargs_name

    RECURSIVE_DECORATOR = "recursive_decorator"

    CALL_TYPES = CALL_FUNCTION | CALL_FUNCTION_VAR | CALL_FUNCTION_KW | \
                 CALL_FUNCTION_VAR_KW

    @pattern(CALL_TYPES)
    def _call_transformer(self, call):
        """"""
        function_argument_count = call.positional + 2 * call.keyword

        if type(call) in (CALL_FUNCTION_VAR, CALL_FUNCTION_KW):
            function_argument_count += 1

        elif type(call) is CALL_FUNCTION_VAR_KW:
            function_argument_count += 2

        # Make tuple of all function args
        yield BUILD_TUPLE(function_argument_count)
        # Switch between function and args
        yield ROT_TWO()
        # Apply recursive_decorator on dec
        yield LOAD_GLOBAL(self.RECURSIVE_DECORATOR)
        yield LOAD_GLOBAL(self.decorator_name)
        yield LOAD_GLOBAL(self.decorator_args_name)
        yield LOAD_GLOBAL(self.decorator_kwargs_name)

        yield CALL_FUNCTION_VAR_KW(1)

        # Apply recursive_decorator(dec) on function
        yield ROT_TWO()
        yield CALL_FUNCTION(1)
        # Switch function and tuple of args
        yield ROT_TWO()
        # Unpack args in the same order they supplied
        yield UNPACK_SEQUENCE(function_argument_count)
        yield BUILD_TUPLE(function_argument_count)
        yield UNPACK_SEQUENCE(function_argument_count)
        # Call function
        yield call
