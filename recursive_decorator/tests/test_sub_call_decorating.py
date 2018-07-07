"""unittest for recursive_decorator."""
import mock
import pytest

from recursive_decorator.recursive_decorator import recursive_decorator


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

# TODO: Check sub_call have params


def test_apply_decorator_for_sub_call(mock_decorator):
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


def test_applying_decorator_with_args_on_sub_call(mock_decorator, mock_wrapper):
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


def test_applying_decorator_with_kwargs_on_sub_call(mock_decorator, mock_wrapper):
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
