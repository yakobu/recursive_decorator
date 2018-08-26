Recursive Decorator
===================

.. image:: https://img.shields.io/pypi/pyversions/Django.svg
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/recursive-decorator/
.. image:: https://badge.fury.io/py/recursive-decorator.svg
    :target: https://badge.fury.io/py/recursive-decorator
.. image:: https://travis-ci.org/yakobu/recursive_decorator.svg?branch=master
    :target: https://travis-ci.org/yakobu/recursive_decorator
.. image:: https://coveralls.io/repos/github/yakobu/recursive_decorator/badge.svg?branch=master
    :target: https://coveralls.io/github/yakobu/recursive_decorator?branch=master



Decorator to apply a given decorator recursively on all function, inside a function/method, recursively.

What is ``recursive_decorator``?
--------------------------------

``recursive_decorator`` is a decorator that allows us to **decorate/trasform all functions along the stack call** at runtime, motivated by the need to add/transform logics, to known\unknown functions, along the stack calls.

Notes:
++++++
* Functions/Methods will not be replaced, new instances will be returned.
* Function/Methods cannot be wrapped more then once with same transformer/decorator.


Installing
----------
.. code-block:: console

    $ pip install recursive_decorator


Usage
-----
import recursive_decorator

.. code-block:: python

    from recursive_decorator import recursive_decorator

define your decorator to apply recursively on all functions.

.. code-block:: python

   >>> def decorator(f):
   ...:    def wrapper(*args, **kwargs):
   ...:        print(f.__name__)
   ...:        return f(*args, **kwargs)
   ...:    return wrapper


Now using your decorator on function without using recursive_decorator will leads to the following output

.. code-block:: python

   >>> @decorator
   ...:def main_function():
   ...:   sub_function()

   >>> main_function()
   main_function


Using recursive_decorator leads to

.. code-block:: python

   >>> @recursive_decorator(decorator)
   ...:def main_function():
   ...:   sub_function()

   >>> main_function()
   main_function
   sub_function


Furthermore, if sub_function has function calls, they will decorated to

.. code-block:: python

   >>> def sub_function():
   ...:    another_function()

   >>> @recursive_decorator(decorator)
   ...:def main_function():
   ...:   sub_function()

   >>> main_function()
   main_function
   sub_function
   another_function


and so on...


Examples
--------

Stop on Execption
+++++++++++++++++

We can wrap all functions with try except...

.. code-block:: python

       >>> import sys
       >>> import ipdb
       >>> from recursive_decorator import recursive_decorator

       >>> def wrap_function_with_try_except(f):
       ...:    def transformed_func(*args, **kwargs):
       ...:        try:
       ...:            return f(*args, **kwargs)
       ...:        except:
       ...:            ipdb.set_trace(sys._getframe().f_back)
       ...:    return transformed_func

       >>> def throws_exception():
       ...:    raise Exception


       >>> @recursive_decorator(wrap_function_with_try_except)
       ...:def function():
       ...:    throws_exception()
       ...:    pass

       >>> function()
          21     throws_exception()
     ---> 22     pass
          23

If function will throw an error... ipdb session will start.


Profiler
++++++++

We can set time profiler for all running functions.

.. code-block:: python

   >>> import time

   >>> from recursive_decorator import recursive_decorator


   >>> def duration_transformer(f):
   ...:    def transformed_func(*args, **kwargs):
   ...:        start_time = time.time()
   ...:        value = f(*args, **kwargs)
   ...:        end_time = time.time()
   ...:        print("function {} duration is {} minutes"
   ...:              .format(f.__name__, end_time - start_time))
   ...:        return value
   ...:    return transformed_func


   >>> def waiting_function():
   ...:    time.sleep(5)


   >>> @recursive_decorator(duration_transformer)
   ...:def function():
   ...:    waiting_function()

   >>> function()
   function waiting_function duration is 5.00511908531189 minutes
   function function duration is 5.006134510040283 minutes

