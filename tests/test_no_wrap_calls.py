"""Validating recursive_decorator is not wrapping unneeded calls."""
import mock
import pytest

from recursive_decorator import recursive_decorator


@pytest.fixture()
def mock_decorator():
    decorator = mock.MagicMock()
    decorator.__name__ = 'mock_decorator1'

    return decorator


def test_apply_decorator_on_builtin_function_or_method(mock_decorator):
    mock_decorator.return_value = None

    assert print == recursive_decorator(mock_decorator)(print)


def test_apply_decorator_on_type(mock_decorator):
    mock_decorator.return_value = None

    assert tuple == recursive_decorator(mock_decorator)(tuple)


def test_apply_decorator_on_module(mock_decorator):
    mock_decorator.return_value = None

    import inspect

    assert inspect == recursive_decorator(mock_decorator)(inspect)


def test_apply_decorator_on_method(mock_decorator):
    mock_decorator.return_value = None

    class A:
        def __init__(self):
            pass

        def method(self):
            pass

    method = A().method

    assert method == recursive_decorator(mock_decorator)(method)
