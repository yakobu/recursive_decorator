"""Validating recursive_decorator transform CALL_FUNCTION instructions."""
import mock
import pytest

from recursive_decorator.recursive_decorator import recursive_decorator


@pytest.fixture()
def mock_decorator1():
    decorator = mock.MagicMock()
    decorator.__name__ = 'mock_decorator1'

    return decorator


@pytest.fixture()
def mock_decorator2():
    decorator = mock.MagicMock()
    decorator.__name__ = 'mock_decorator2'

    return decorator


def test_apply_decorator_on_call_that_should_not_be_wrapped(mock_decorator1):
    mock_decorator1.side_effect = lambda func: func

    class A:
        def __init__(self):
            pass

        def method(self):
            pass

    method = A().method

    assert abs == recursive_decorator(mock_decorator1)(abs)
    assert tuple == recursive_decorator(mock_decorator1)(tuple)
    assert A == recursive_decorator(mock_decorator1)(A)
    assert method == recursive_decorator(mock_decorator1)(method)


def test_apply_decorator_on_recursive_function(mock_decorator1):
    mock_decorator1.side_effect = lambda func: func

    @recursive_decorator(mock_decorator1)
    def func_to_decorate(num=5):
        if num == 1:
            return

        func_to_decorate(num - 1)

    func_to_decorate()

    mock_decorator1.assert_called_once()


def test_apply_decorator_on_function_with_recursive_sub_call(mock_decorator1):
    mock_decorator1.side_effect = lambda func: func

    def another_func(num=5):
        if num == 1:
            return

        another_func(num - 1)

    @recursive_decorator(mock_decorator1)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func()

    mock_decorator1.assert_called_once()

    func_to_decorate()

    assert mock_decorator1.call_count == 6
    assert func_to_decorate.has_been_called is True


def test_wrapping_sub_call_which_already_wrapped_with_same_decorator(
        mock_decorator1):
    mock_decorator1.side_effect = lambda func: func

    @recursive_decorator(mock_decorator1)
    def another_func():
        another_func.has_been_called = True

    @recursive_decorator(mock_decorator1)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func()

        assert mock_decorator1.call_count == 2

    func_to_decorate()

    assert mock_decorator1.call_count == 2
    assert func_to_decorate.has_been_called is True
    assert another_func.has_been_called is True


def test_wrapping_sub_call_which_already_wrapped_with_another_decorator(
        mock_decorator1, mock_decorator2):
    mock_decorator1.side_effect = lambda func: func

    @recursive_decorator(mock_decorator1)
    def another_func():
        another_func.has_been_called = True

    @recursive_decorator(mock_decorator2)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func()

    mock_decorator1.assert_called_once()
    mock_decorator2.assert_called_once()

    func_to_decorate()

    mock_decorator2.assert_called_once()
    assert mock_decorator1.call_count == 2
    assert func_to_decorate.has_been_called is True
    assert another_func.has_been_called is True
