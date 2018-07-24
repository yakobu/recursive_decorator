"""Validating recursive_decorator doesn't break normal usage of decorator."""
import mock
import pytest

from recursive_decorator import recursive_decorator
from recursive_decorator.utils import DECORATOR_LIST_FIELD_NAME


@pytest.fixture()
def mock_decorator():
    decorator = mock.MagicMock()
    decorator.__name__ = 'mock_decorator'

    return decorator


@pytest.fixture()
def mock_wrapper():
    # Set mocking decorator
    wrapper = mock.MagicMock()
    wrapper.__name__ = 'wrapper'
    # Identity function
    wrapper.side_effect = lambda func: func

    return wrapper


def test_applying_decorator(mock_decorator):
    mock_decorator.side_effect = lambda func: func

    @recursive_decorator(mock_decorator)
    def func_to_decorate():
        func_to_decorate.has_been_called = True

    mock_decorator.assert_called_once()

    func_to_decorate()

    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_default_kwargs(mock_decorator):
    mock_decorator.side_effect = lambda func: func
    kwdefaults_value = 3

    @recursive_decorator(mock_decorator)
    def func_to_decorate(*, k=kwdefaults_value):
        func_to_decorate.kwdefaults = k

    mock_decorator.assert_called_once()

    func_to_decorate()

    assert func_to_decorate.kwdefaults == kwdefaults_value


def test_applying_decorator_on_function_with_args(mock_decorator):
    mock_decorator.side_effect = lambda func: func
    args = (1, "2")

    @recursive_decorator(mock_decorator)
    def func_to_decorate(x, y):
        func_to_decorate.args = (x, y)

    mock_decorator.assert_called_once()

    func_to_decorate(*args)

    assert func_to_decorate.args == args


def test_applying_decorator_on_function_with_asterisk_args(mock_decorator):
    mock_decorator.side_effect = lambda func: func
    args = (1, "2")

    @recursive_decorator(mock_decorator)
    def func_to_decorate(*args):
        func_to_decorate.args = args

    mock_decorator.assert_called_once()

    func_to_decorate(*args)

    assert func_to_decorate.args == args


def test_applying_decorator_on_function_with_kwargs(mock_decorator):
    mock_decorator.side_effect = lambda func: func
    func_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator)
    def func_to_decorate(a, c, b, d):
        func_to_decorate.kwargs = {"a": a, "c": c, "b": b, "d": d}

    mock_decorator.assert_called_once()

    func_to_decorate(**func_kwargs)

    assert func_to_decorate.kwargs == func_kwargs


def test_applying_decorator_on_function_with_asterisk_kwargs(mock_decorator):
    mock_decorator.side_effect = lambda func: func
    func_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator)
    def func_to_decorate(**kwargs):
        func_to_decorate.kwargs = kwargs

    mock_decorator.assert_called_once()

    func_to_decorate(**func_kwargs)

    assert func_to_decorate.kwargs == func_kwargs


def test_applying_decorator_with_args(mock_decorator, mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    args = (1, 2, 'a', "b")

    @recursive_decorator(mock_decorator, *args)
    def func_to_decorate():
        func_to_decorate.has_been_called = True

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*args)

    func_to_decorate()

    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_args_on_function_with_args(mock_decorator,
                                                            mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    decorator_args = (1, 2, 'a', "b")
    func_args = (6, 7, 'c', "d")

    @recursive_decorator(mock_decorator, *decorator_args)
    def func_to_decorate(x, y, z, w):
        func_to_decorate.args = (x, y, z, w)

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*decorator_args)

    func_to_decorate(*func_args)

    assert func_to_decorate.args == func_args


def test_applying_decorator_with_args_on_function_with_asterisk_args(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    decorator_args = (1, 2, 'a', "b")
    func_args = (6, 7, 'c', "d")

    @recursive_decorator(mock_decorator, *decorator_args)
    def func_to_decorate(*args):
        func_to_decorate.args = args

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*decorator_args)

    func_to_decorate(*func_args)

    assert func_to_decorate.args == func_args


def test_applying_decorator_with_args_on_function_with_kwargs(mock_decorator,
                                                              mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    decorator_args = (1, 2, 'a', "b")
    func_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, *decorator_args)
    def func_to_decorate(a, c, b, d):
        func_to_decorate.kwargs = {"a": a, "c": c, "b": b, "d": d}

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*decorator_args)

    func_to_decorate(**func_kwargs)

    assert func_to_decorate.kwargs == func_kwargs


def test_applying_decorator_with_args_on_function_with_asterisk_kwargs(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    decorator_args = (1, 2, 'a', "b")
    func_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, *decorator_args)
    def func_to_decorate(**func_kwargs):
        func_to_decorate.kwargs = func_kwargs

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*decorator_args)

    func_to_decorate(**func_kwargs)

    assert func_to_decorate.kwargs == func_kwargs


def test_applying_decorator_with_kwargs(mock_decorator, mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, **kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(**kwargs)

    func_to_decorate()

    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_kwargs_on_function_with_args(mock_decorator,
                                                              mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    function_args = (1, "2")
    decorator_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, **decorator_kwargs)
    def func_to_decorate(x, y):
        func_to_decorate.args = (x, y)

    mock_decorator.assert_called_once()

    func_to_decorate(*function_args)

    assert func_to_decorate.args == function_args


def test_applying_decorator_with_kwargs_on_function_with_asterisk_args(
        mock_decorator, mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    function_args = (1, "2")
    decorator_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, **decorator_kwargs)
    def func_to_decorate(*args):
        func_to_decorate.args = args

    mock_decorator.assert_called_once()

    func_to_decorate(*function_args)

    assert func_to_decorate.args == function_args


def test_applying_decorator_with_kwargs_on_function_with_kwargs(mock_decorator,
                                                                mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    func_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}
    decorator_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, **decorator_kwargs)
    def func_to_decorate(a, c, b, d):
        func_to_decorate.kwargs = {"a": a, "c": c, "b": b, "d": d}

    mock_decorator.assert_called_once()

    func_to_decorate(**func_kwargs)

    assert func_to_decorate.kwargs == func_kwargs


def test_applying_decorator_with_kwargs_on_function_with_asterisk_kwargs(
        mock_decorator, mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    func_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}
    decorator_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, **decorator_kwargs)
    def func_to_decorate(**kwargs):
        func_to_decorate.kwargs = kwargs

    mock_decorator.assert_called_once()

    func_to_decorate(**func_kwargs)

    assert func_to_decorate.kwargs == func_kwargs


def test_applying_decorator_with_args_and_kwargs(mock_decorator, mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    args = (1, 2, 'a', "b")
    kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, *args, **kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*args, **kwargs)

    func_to_decorate()

    assert func_to_decorate.has_been_called is True


#



def test_applying_decorator_with_args_and_kwargs_on_function_with_args(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    function_args = (1, "2")
    decorator_args = (1, 2, 'a', "b")
    decorator_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, *decorator_args, **decorator_kwargs)
    def func_to_decorate(x, y):
        func_to_decorate.args = (x, y)

    mock_decorator.assert_called_once()

    func_to_decorate(*function_args)

    assert func_to_decorate.args == function_args


def test_applying_decorator_with_args_and_kwargs_on_function_with_asterisk_args(
        mock_decorator, mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    function_args = (1, "2")
    decorator_args = (1, 2, 'a', "b")
    decorator_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, *decorator_args, **decorator_kwargs)
    def func_to_decorate(*args):
        func_to_decorate.args = args

    mock_decorator.assert_called_once()

    func_to_decorate(*function_args)

    assert func_to_decorate.args == function_args


def test_applying_decorator_with_args_and_kwargs_on_function_with_kwargs(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    func_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}
    decorator_args = (1, 2, 'a', "b")
    decorator_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, *decorator_args, **decorator_kwargs)
    def func_to_decorate(a, c, b, d):
        func_to_decorate.kwargs = {"a": a, "c": c, "b": b, "d": d}

    mock_decorator.assert_called_once()

    func_to_decorate(**func_kwargs)

    assert func_to_decorate.kwargs == func_kwargs


def test_applying_decorator_with_args_and_kwargs_on_function_with_asterisk_kwargs(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    func_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}
    decorator_args = (1, 2, 'a', "b")
    decorator_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    @recursive_decorator(mock_decorator, *decorator_args, **decorator_kwargs)
    def func_to_decorate(**kwargs):
        func_to_decorate.kwargs = kwargs

    mock_decorator.assert_called_once()

    func_to_decorate(**func_kwargs)

    assert func_to_decorate.kwargs == func_kwargs


def test_wrapped_value_when_decorator_change_function(mock_decorator):
    def another_func():
        pass

    mock_decorator.side_effect = lambda func: another_func

    @recursive_decorator(mock_decorator)
    def func_to_decorate():
        pass

    func_after_decorating_list = getattr(func_to_decorate,
                                         DECORATOR_LIST_FIELD_NAME)
    assert func_after_decorating_list == ["mock_decorator"]


def test_wrapped_value_when_decorator_change_method(mock_decorator):
    class A:
        def __init__(self):
            pass

        def method(self):
            pass

        def another_method(self):
            pass

    instance = A()
    method = instance.method
    another_method = instance.another_method

    mock_decorator.side_effect = lambda method: another_method

    decorated_method = recursive_decorator(mock_decorator)(method)

    func_after_decorating_list = getattr(decorated_method,
                                         DECORATOR_LIST_FIELD_NAME)

    assert func_after_decorating_list == ["mock_decorator"]
