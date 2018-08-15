Recursive Decorator
==========================
[![Build Status](https://travis-ci.org/yakobu/recursive_decorator.svg?branch=master)](https://travis-ci.org/yakobu/recursive_decorator)
[![Coverage Status](https://coveralls.io/repos/github/yakobu/recursive_decorator/badge.svg?branch=master)](https://coveralls.io/github/yakobu/recursive_decorator?branch=master)

Decorator to apply a given decorator recursively on all function, inside a function/method, recursively.

What is ``recursive_decorator``?
----------------------------

``recursive_decorator`` is a decorator that allows us to **decorate/transform** function at runtime, motivated by the need to add/transform logics, to known\unknown functions, along the stack calls.

#### Notes:
* Functions/Methods will not be replaced, new instances will be returned.
* Function/Methods cannot be wrapped more then once with same transformer/decorator.

Examples:
---------

### Print Stack Calls

```python
   >>> from recursive_decorator import recursive_decorator 
   
   >>> def print_function_name_transformer(f):
   ...:    def transformed_func(*args, **kwargs):
   ...:        print(f.__name__)
   ...:        return f(*args, **kwargs)
   ...:    return transformed_func
   
   
   >>> def third():
   ...:    pass

   >>> def second():
   ...:    third()

   >>>  @recursive_decorator(print_function_name_transformer)
   ...: def first():
   ...:     second()
   
   >>> first()
    first
    second
    third
```

### Stop on Execption

```python
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
   ...:    print("still will be called after continue!!!")
 
    >>> function()
     21     throws_exception()
---> 22     print("still will be called after continue!!!")
     23 


   
   ```
   
### Calculate Duration
   
   ```python
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
   ...:    def function():
   ...:        waiting_function()
   
   >>> function()
   function waiting_function duration is 5.00511908531189 minutes
   function function duration is 5.006134510040283 minutes

   
   
   ```
