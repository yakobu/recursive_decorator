"""Validating recursive_decorator transform CALL_FUNCTION instructions."""
import mock
import pytest

from recursive_decorator import recursive_decorator


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


def test_apply_decorator_on_call_function(mock_decorator):
    mock_decorator.side_effect = lambda func: func

    def another_func():
        another_func.has_been_called = True

    @recursive_decorator(mock_decorator)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func()

    mock_decorator.assert_called_once()

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert another_func.has_been_called is True
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_args_on_call_function(mock_decorator,
                                                       mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    args = (1, 2, 'a', "b")

    def another_func():
        another_func.has_been_called = True

    @recursive_decorator(mock_decorator, *args)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func()

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*args)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.has_been_called is True
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_kwargs_on_call_function(mock_decorator,
                                                         mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    def another_func():
        another_func.has_been_called = True

    @recursive_decorator(mock_decorator, **kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func()

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(**kwargs)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.has_been_called is True
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_args_and_kwargs_on_call_function(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    args = (1, 2, 'a', "b")
    kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    def another_func():
        another_func.has_been_called = True

    @recursive_decorator(mock_decorator, *args, **kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func()

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*args, **kwargs)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.has_been_called is True
    assert func_to_decorate.has_been_called is True


def test_apply_decorator_on_call_function_with_positional_args(mock_decorator):
    mock_decorator.side_effect = lambda func: func

    def another_func(*args):
        another_func.args = args

    @recursive_decorator(mock_decorator)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3')

    mock_decorator.assert_called_once()

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert another_func.args == (1, 2, '3')
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_args_on_call_function_with_positional_args(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    args = (1, 2, 'a', "b")

    def another_func(*args):
        another_func.args = args

    @recursive_decorator(mock_decorator, *args)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3')

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*args)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.args == (1, 2, '3')
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_kwargs_on_call_function_with_positional_args(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    def another_func(*args):
        another_func.args = args

    @recursive_decorator(mock_decorator, **kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3')

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(**kwargs)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.args == (1, 2, '3')
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_args_and_kwargs_on_call_function_with_positional_args(
        mock_decorator, mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    args = (1, 2, 'a', "b")
    kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    def another_func(*args):
        another_func.args = args

    @recursive_decorator(mock_decorator, *args, **kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3')

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*args, **kwargs)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.args == (1, 2, '3')
    assert func_to_decorate.has_been_called is True


def test_apply_decorator_on_call_function_with_keyword(mock_decorator):
    mock_decorator.side_effect = lambda func: func

    def another_func(**kwargs):
        another_func.kwargs = kwargs

    @recursive_decorator(mock_decorator)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(a=1, b=2, c='3')

    mock_decorator.assert_called_once()

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert another_func.kwargs == {'a': 1, 'b': 2, 'c': '3'}
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_args_on_call_function_with_keyword(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    args = (1, 2, 'a', "b")

    def another_func(**kwargs):
        another_func.kwargs = kwargs

    @recursive_decorator(mock_decorator, *args)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(a=1, b=2, c='3')

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*args)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.kwargs == {'a': 1, 'b': 2, 'c': '3'}
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_kwargs_on_call_function_with_keyword(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    def another_func(**kwargs):
        another_func.kwargs = kwargs

    @recursive_decorator(mock_decorator, **kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(a=1, b=2, c='3')

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(**kwargs)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.kwargs == {'a': 1, 'b': 2, 'c': '3'}
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_args_and_kwargs_on_call_function_with_keyword(
        mock_decorator, mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    args = (1, 2, 'a', "b")
    kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    def another_func(**kwargs):
        another_func.kwargs = kwargs

    @recursive_decorator(mock_decorator, *args, **kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(a=1, b=2, c='3')

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*args, **kwargs)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.kwargs == {'a': 1, 'b': 2, 'c': '3'}
    assert func_to_decorate.has_been_called is True


def test_apply_decorator_on_call_function_with_positional_args_and_keyword(
        mock_decorator):
    mock_decorator.side_effect = lambda func: func

    def another_func(*args, **kwargs):
        another_func.args = args
        another_func.kwargs = kwargs

    @recursive_decorator(mock_decorator)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3', a=1, b=2, c='3')

    mock_decorator.assert_called_once()

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert another_func.args == (1, 2, '3')
    assert another_func.kwargs == {'a': 1, 'b': 2, 'c': '3'}
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_args_on_call_function_with_positional_args_and_keyword(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    args = (1, 2, 'a', "b")

    def another_func(*args, **kwargs):
        another_func.args = args
        another_func.kwargs = kwargs

    @recursive_decorator(mock_decorator, *args)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3', a=1, b=2, c='3')

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*args)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.args == (1, 2, '3')
    assert another_func.kwargs == {'a': 1, 'b': 2, 'c': '3'}
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_kwargs_on_call_function_with_positional_args_and_keyword(
        mock_decorator,
        mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    def another_func(*args, **kwargs):
        another_func.args = args
        another_func.kwargs = kwargs

    @recursive_decorator(mock_decorator, **kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3', a=1, b=2, c='3')

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(**kwargs)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.args == (1, 2, '3')
    assert another_func.kwargs == {'a': 1, 'b': 2, 'c': '3'}
    assert func_to_decorate.has_been_called is True


def test_applying_decorator_with_args_and_kwargs_on_call_function_with_positional_args_and_keyword(
        mock_decorator, mock_wrapper):
    mock_decorator.return_value = mock_wrapper
    args = (1, 2, 'a', "b")
    kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}

    def another_func(*args, **kwargs):
        another_func.args = args
        another_func.kwargs = kwargs

    @recursive_decorator(mock_decorator, *args, **kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3', a=1, b=2, c='3')

    mock_wrapper.assert_called_once()
    mock_decorator.assert_called_once_with(*args, **kwargs)

    func_to_decorate()

    assert mock_decorator.call_count == 2
    assert mock_wrapper.call_count == 2
    assert another_func.args == (1, 2, '3')
    assert another_func.kwargs == {'a': 1, 'b': 2, 'c': '3'}
    assert func_to_decorate.has_been_called is True
