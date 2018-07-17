"""Validating decorating with recursive_decorator more then once."""
import mock
import pytest

from recursive_decorator import recursive_decorator


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


@pytest.fixture()
def mock_wrapper1():
    # Set mocking decorator
    wrapper = mock.MagicMock()
    wrapper.__name__ = 'wrapper'
    # Identity function
    wrapper.side_effect = lambda func: func

    return wrapper


@pytest.fixture()
def mock_wrapper2():
    # Set mocking decorator
    wrapper = mock.MagicMock()
    wrapper.__name__ = 'wrapper'
    # Identity function
    wrapper.side_effect = lambda func: func

    return wrapper


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
    mock_decorator2.side_effect = lambda func: func

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

    mock_decorator1.assert_called_once()
    assert mock_decorator2.call_count == 2
    assert func_to_decorate.has_been_called is True
    assert another_func.has_been_called is True


def test_wrapping_function_twice(mock_decorator1, mock_decorator2):
    mock_decorator1.side_effect = lambda func: func
    mock_decorator2.side_effect = lambda func: func

    @recursive_decorator(mock_decorator2)
    @recursive_decorator(mock_decorator1)
    def func_to_decorate():
        func_to_decorate.has_been_called = True

    mock_decorator1.assert_called_once()
    mock_decorator2.assert_called_once()

    func_to_decorate()

    mock_decorator1.assert_called_once()
    mock_decorator2.assert_called_once()
    assert func_to_decorate.has_been_called is True


def test_wrapping_function_twice_with_sub_call(
        mock_decorator1, mock_decorator2):
    mock_decorator1.side_effect = lambda func: func
    mock_decorator2.side_effect = lambda func: func

    def another_func():
        another_func.has_been_called = True

    @recursive_decorator(mock_decorator2)
    @recursive_decorator(mock_decorator1)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func()

    mock_decorator1.assert_called_once()
    mock_decorator2.assert_called_once()

    func_to_decorate()

    assert mock_decorator1.call_count == 2
    assert mock_decorator2.call_count == 2
    assert func_to_decorate.has_been_called is True
    assert another_func.has_been_called is True


def test_wrapping_function_twice_with_args_and_kwargs_on_call_function_with_positional_args_and_keyword(
        mock_decorator1, mock_decorator2, mock_wrapper1, mock_wrapper2):
    mock_decorator1.return_value = mock_wrapper1
    mock_decorator2.return_value = mock_wrapper2
    decorator1_args = (1, 2, 'a', "b")
    decorator1_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}
    decorator2_args = (5, 13, 'a11', "33b")
    decorator2_kwargs = {'a': 55, 'c': '11', 'b': 22, 'd': '12'}
    mock_decorator1_calls = [mock.call(*decorator1_args,
                                       **decorator1_kwargs)] * 2
    mock_decorator2_calls = [mock.call(*decorator2_args,
                                       **decorator2_kwargs)] * 2

    def another_func(*args, **kwargs):
        another_func.args = args
        another_func.kwargs = kwargs

    @recursive_decorator(mock_decorator2, *decorator2_args, **decorator2_kwargs)
    @recursive_decorator(mock_decorator1, *decorator1_args, **decorator1_kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3', a=1, b=2, c='3')

    mock_wrapper1.assert_called_once()
    mock_wrapper2.assert_called_once()
    mock_decorator1.assert_called_once_with(*decorator1_args,
                                            **decorator1_kwargs)
    mock_decorator2.assert_called_once_with(*decorator2_args,
                                            **decorator2_kwargs)

    func_to_decorate()

    mock_decorator1.assert_has_calls(mock_decorator1_calls, any_order=True)
    mock_decorator2.assert_has_calls(mock_decorator2_calls, any_order=True)

    assert mock_decorator1.call_count == 2
    assert mock_decorator2.call_count == 2
    assert mock_wrapper1.call_count == 2
    assert mock_wrapper2.call_count == 2
    assert another_func.args == (1, 2, '3')
    assert another_func.kwargs == {'a': 1, 'b': 2, 'c': '3'}
    assert func_to_decorate.has_been_called is True


def test_wrapping_function_twice_with_args_and_kwargs_on_call_function_kw_with_positional_args_and_keyword(
        mock_decorator1, mock_decorator2, mock_wrapper1, mock_wrapper2):
    mock_decorator1.return_value = mock_wrapper1
    mock_decorator2.return_value = mock_wrapper2
    decorator1_args = (1, 2, 'a', "b")
    decorator1_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}
    decorator2_args = (5, 13, 'a11', "33b")
    decorator2_kwargs = {'a': 55, 'c': '11', 'b': 22, 'd': '12'}
    another_func_kwargs = {'e': 1, 'f': '1'}
    mock_decorator1_calls = [mock.call(*decorator1_args,
                                       **decorator1_kwargs)] * 2
    mock_decorator2_calls = [mock.call(*decorator2_args,
                                       **decorator2_kwargs)] * 2

    def another_func(*args, **kwargs):
        another_func.kwargs = kwargs
        another_func.args = args

    @recursive_decorator(mock_decorator2, *decorator2_args, **decorator2_kwargs)
    @recursive_decorator(mock_decorator1, *decorator1_args, **decorator1_kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3', a=1, b=2, c='3', **another_func_kwargs)

    mock_wrapper1.assert_called_once()
    mock_wrapper2.assert_called_once()
    mock_decorator1.assert_called_once_with(*decorator1_args,
                                            **decorator1_kwargs)
    mock_decorator2.assert_called_once_with(*decorator2_args,
                                            **decorator2_kwargs)

    func_to_decorate()

    mock_decorator1.assert_has_calls(mock_decorator1_calls, any_order=True)
    mock_decorator2.assert_has_calls(mock_decorator2_calls, any_order=True)

    assert mock_decorator1.call_count == 2
    assert mock_wrapper1.call_count == 2
    assert another_func.args == (1, 2, '3')
    assert another_func.kwargs == dict({'a': 1, 'b': 2, 'c': '3'},
                                       **another_func_kwargs)
    assert func_to_decorate.has_been_called is True


def test_wrapping_function_twice_with_args_and_kwargs_on_call_function_var_with_positional_args_and_keyword(
        mock_decorator1, mock_decorator2, mock_wrapper1, mock_wrapper2):
    mock_decorator1.return_value = mock_wrapper1
    mock_decorator2.return_value = mock_wrapper2
    decorator1_args = (1, 2, 'a', "b")
    decorator1_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}
    another_func_args = (7, 4, '3')
    decorator2_args = (5, 13, 'a11', "33b")
    decorator2_kwargs = {'a': 55, 'c': '11', 'b': 22, 'd': '12'}
    mock_decorator1_calls = [mock.call(*decorator1_args,
                                       **decorator1_kwargs)] * 2
    mock_decorator2_calls = [mock.call(*decorator2_args,
                                       **decorator2_kwargs)] * 2

    def another_func(*args, **kwargs):
        another_func.kwargs = kwargs
        another_func.args = args

    @recursive_decorator(mock_decorator2, *decorator2_args, **decorator2_kwargs)
    @recursive_decorator(mock_decorator1, *decorator1_args, **decorator1_kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3', a=1, b=2, c='3', *another_func_args)

    mock_wrapper1.assert_called_once()
    mock_wrapper2.assert_called_once()
    mock_decorator1.assert_called_once_with(*decorator1_args,
                                            **decorator1_kwargs)
    mock_decorator2.assert_called_once_with(*decorator2_args,
                                            **decorator2_kwargs)

    func_to_decorate()

    mock_decorator1.assert_has_calls(mock_decorator1_calls, any_order=True)
    mock_decorator2.assert_has_calls(mock_decorator2_calls, any_order=True)

    assert mock_decorator1.call_count == 2
    assert mock_wrapper1.call_count == 2
    assert another_func.args == (1, 2, '3') + another_func_args
    assert another_func.kwargs == {'a': 1, 'b': 2, 'c': '3'}
    assert func_to_decorate.has_been_called is True


def test_wrapping_function_twice_with_args_and_kwargs_on_call_function_var_kw_with_positional_args_and_keyword(
        mock_decorator1, mock_decorator2, mock_wrapper1, mock_wrapper2):
    mock_decorator1.return_value = mock_wrapper1
    mock_decorator2.return_value = mock_wrapper2
    decorator1_args = (1, 2, 'a', "b")
    decorator1_kwargs = {'a': 1, 'c': '1', 'b': 2, 'd': '2'}
    decorator2_args = (5, 13, 'a11', "33b")
    decorator2_kwargs = {'a': 55, 'c': '11', 'b': 22, 'd': '12'}
    mock_decorator1_calls = [mock.call(*decorator1_args,
                                       **decorator1_kwargs)] * 2
    mock_decorator2_calls = [mock.call(*decorator2_args,
                                       **decorator2_kwargs)] * 2
    another_func_args = (7, 4, '3')
    another_func_kwargs = {'e': 1, 'f': '1'}

    def another_func(*args, **kwargs):
        another_func.kwargs = kwargs
        another_func.args = args

    @recursive_decorator(mock_decorator2, *decorator2_args, **decorator2_kwargs)
    @recursive_decorator(mock_decorator1, *decorator1_args, **decorator1_kwargs)
    def func_to_decorate():
        func_to_decorate.has_been_called = True
        another_func(1, 2, '3', a=1, b=2, c='3', *another_func_args,
                     **another_func_kwargs)

    mock_wrapper1.assert_called_once()
    mock_wrapper2.assert_called_once()
    mock_decorator1.assert_called_once_with(*decorator1_args,
                                            **decorator1_kwargs)
    mock_decorator2.assert_called_once_with(*decorator2_args,
                                            **decorator2_kwargs)

    func_to_decorate()

    mock_decorator1.assert_has_calls(mock_decorator1_calls, any_order=True)
    mock_decorator2.assert_has_calls(mock_decorator2_calls, any_order=True)

    assert mock_decorator1.call_count == 2
    assert mock_wrapper1.call_count == 2
    assert another_func.args == (1, 2, '3') + another_func_args
    assert another_func.kwargs == dict({'a': 1, 'b': 2, 'c': '3'},
                                       **another_func_kwargs)
    assert func_to_decorate.has_been_called is True
