"""
Self Auto-Register classes
"""

import re
from typing import Callable, List, Dict
from agptools.helpers import (
    best_of,
)


def names(klass):
    "return a list of names for a class"
    yield klass.__name__
    yield klass.__module__ + "." + klass.__name__


def match_score(item):
    "score by counting how many groups have matched"
    info, m = item
    sc = len(m.groups())
    return sc, info


class Record:
    factory: Callable
    args: List
    kwargs: Dict


class iRegistry:
    "a registry of objects"

    REGISTRY = {}

    @classmethod
    def register_info(cls, patterns, *args, **kwargs):
        "register a class in the registry"
        __key__ = kwargs.pop("__key__", None)
        __klass__ = kwargs.pop("__klass__", None)
        if isinstance(patterns, str):
            patterns = [patterns]
        for pattern in patterns:
            cls.REGISTRY.setdefault(pattern, {}).setdefault(__klass__, {})[
                __key__
            ] = (
                args,
                kwargs,
            )

    @classmethod
    def register_itself(cls, patterns, *args, **kwargs):
        "register a class in the registry"

        kwargs["__klass__"] = cls
        # args = cls, *args
        cls.register_info(patterns, *args, **kwargs)

    @classmethod
    def locate(cls, thing, __key__=None, __klass__=None, score=None):
        "try to locate some info in the registry"
        candidates = []
        for pattern, info in cls.REGISTRY.items():
            if m := re.search(pattern, thing):
                if __klass__:
                    info = {
                        k: v
                        for k, v in info.items()
                        if issubclass(k, __klass__)
                    }
                if info:
                    candidates.append((info, m))

        score = score or match_score
        _, options = best_of(candidates, score)
        if options:
            __key__ = __key__ if __key__ in options else list(options).pop()
            return __key__, options[__key__]
        return None

    @classmethod
    def get_factory(
        cls, thing, __key__=None, __klass__=None, score=None, **context
    ):
        "Get factory and parameters from the registry"
        option = cls.locate(thing, __key__, __klass__, score)
        if option:
            factory, info = option
            for __key__, (args, kw) in info.items():
                context.update(kw)
                return factory, args, context
        return None, None, None

    @classmethod
    def get_(cls, name):
        "get a class from the registry by name"
        for _name in names(cls):
            if (obj := cls.REGISTRY.get(_name).get(name)) is not None:
                break
        return obj

    @classmethod
    def search_(cls, name):
        "do a full search of a class by name in the whole registry database"
        for values in cls.REGISTRY.values():
            if (obj := values.get(name)) is not None:
                break
        return obj
