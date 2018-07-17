"""Validating decorating recursive function call with recursive_decorator."""
import mock
import pytest

from recursive_decorator import recursive_decorator


@pytest.fixture()
def mock_decorator1():
    decorator = mock.MagicMock()
    decorator.__name__ = 'mock_decorator1'

    return decorator


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
        another_func.call_count += 1
        if num == 1:
            return

        another_func(num - 1)

    another_func.call_count = 0

    @recursive_decorator(mock_decorator1)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func()

    mock_decorator1.assert_called_once()

    func_to_decorate()

    assert another_func.call_count == 5
    assert mock_decorator1.call_count == 6
    assert func_to_decorate.has_been_called is True
