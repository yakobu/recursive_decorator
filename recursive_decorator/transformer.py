"""Call transformer module."""
from codetransformer import CodeTransformer, pattern
from codetransformer.instructions import (CALL_FUNCTION, BUILD_TUPLE, ROT_TWO,
                                          LOAD_GLOBAL, UNPACK_SEQUENCE,CALL_FUNCTION_VAR_KW)


class RecursiveDecoratorCallTransformer(CodeTransformer):
    """Transformer class for every call in function."""
    def __init__(self, decorator_name, decorator_args_name, decorator_kwargs_name):
        self.decorator_name = decorator_name
        self.decorator_args_name = decorator_args_name
        self.decorator_kwargs_name = decorator_kwargs_name

    RECURSIVE_DECORATOR = "recursive_decorator"

    # @pattern(CALL_FUNCTION)
    # def _call_function(self, call):
    #     """"""
    #     # Make tuple of all function args
    #     yield BUILD_TUPLE(call.arg)
    #     # Switch between function and args
    #     yield ROT_TWO()
    #     # Apply recursive_decorator on dec
    #     yield LOAD_GLOBAL(self.RECURSIVE_DECORATOR)
    #     yield LOAD_GLOBAL(self.decorator_name)
    #     yield CALL_FUNCTION(1)
    #     # Apply recursive_decorator(dec) on function
    #     yield ROT_TWO()
    #     yield CALL_FUNCTION(1)
    #     # Switch function and tuple of args
    #     yield ROT_TWO()
    #     # Unpack args in the same order they supplied
    #     yield UNPACK_SEQUENCE(call.arg)
    #     yield BUILD_TUPLE(call.arg)
    #     yield UNPACK_SEQUENCE(call.arg)
    #     # Call function
    #     yield call


    @pattern(CALL_FUNCTION)
    def _call_function(self, call):
        """"""
        # Make tuple of all function args
        yield BUILD_TUPLE(call.positional + 2 * call.keyword)
        # Switch between function and args
        yield ROT_TWO()
        # Apply recursive_decorator on dec
        #
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
        yield UNPACK_SEQUENCE(call.positional + 2 * call.keyword)
        yield BUILD_TUPLE(call.positional + 2 * call.keyword)
        yield UNPACK_SEQUENCE(call.positional + 2 * call.keyword)
        # Call function
        yield call
