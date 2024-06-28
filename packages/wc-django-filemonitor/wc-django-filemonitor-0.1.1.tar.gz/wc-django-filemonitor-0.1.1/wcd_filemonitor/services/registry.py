from typing import *


__all__ = 'registry', 'is_registered', 'add', 'remove', 'items',

registry = dict()


def is_registered(key: str):
    return key in registry


def add(key: str, patterns: List[str], handler: Callable):
    if is_registered(key):
        raise KeyError(f'Configuration for "{key}" already added.')

    registry[key] = (patterns, handler)


def remove(key: str):
    if not is_registered(key):
        raise KeyError(f'No configuration found for "{key}" key.')

    registry.pop(key)


def items():
    for key, (patterns, handler) in registry.items():
        yield key, patterns, handler
