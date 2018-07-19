"""Utilities for recursive decorator."""


def mount_function_to_module(module, function):
    """Mount Given function to given module.

    Args:
        module(module): module to mount function.
        function(function): function to mount.
    """
    setattr(module, function.__name__, function)
