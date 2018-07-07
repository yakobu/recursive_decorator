"""Call transformer module."""
from codetransformer import CodeTransformer, pattern
from codetransformer.instructions import (CALL_FUNCTION, BUILD_TUPLE, ROT_TWO,
                                          LOAD_GLOBAL, UNPACK_SEQUENCE)


class RecursiveDecoratorCallTransformer(CodeTransformer):
    """Transformer class for every call in function."""
    def __init__(self, decorator_name, decorator_params_name, decorator_params_count):
        self.decorator_name = decorator_name
        self.decorator_params_name = decorator_params_name
        self.decorator_params_count = decorator_params_count

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
        print("decorator_params_name:", self.decorator_params_name)
        print("decorator_name:", self.decorator_name)
        print("decorator_params_count:", self.decorator_params_count)

        # Make tuple of all function args
        yield BUILD_TUPLE(call.arg)
        # Switch between function and args
        yield ROT_TWO()
        # Apply recursive_decorator on dec
        #
        yield LOAD_GLOBAL(self.RECURSIVE_DECORATOR)
        yield LOAD_GLOBAL(self.decorator_name)
        yield LOAD_GLOBAL(self.decorator_params_name)
        yield UNPACK_SEQUENCE(self.decorator_params_count)
        yield BUILD_TUPLE(self.decorator_params_count)
        yield UNPACK_SEQUENCE(self.decorator_params_count)
        yield CALL_FUNCTION(self.decorator_params_count + 1)

        # Apply recursive_decorator(dec) on function
        yield ROT_TWO()
        yield CALL_FUNCTION(1)
        # Switch function and tuple of args
        yield ROT_TWO()
        # Unpack args in the same order they supplied
        yield UNPACK_SEQUENCE(call.arg)
        yield BUILD_TUPLE(call.arg)
        yield UNPACK_SEQUENCE(call.arg)
        # Call function
        yield call
