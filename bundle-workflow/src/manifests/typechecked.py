# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# from https://gist.github.com/svermeulen/8a6ad727113a6d07f78332152c1d33b2
#

from dataclasses import dataclass, is_dataclass

import typeguard
from typeguard import typechecked


@typechecked
def _add_validate_member_types_method(cls: type):
    def _validate_member_types(self):
        for member_name, member_type in cls.__annotations__.items():
            member_value = getattr(self, member_name)
            typeguard.check_type(member_name, member_value, member_type)

    assert not hasattr(cls, "_validate_member_types")
    cls._validate_member_types = _validate_member_types  # type:ignore


@typechecked
def _override_set_state_method(cls: type):
    old_set_state = getattr(cls, "__setstate__", None)

    # Override setstate so that we detect when errors occur during unpickling
    def setstate(self, d):
        if old_set_state is not None:
            old_set_state(self, d)
        else:
            self.__dict__ = d
        self._validate_member_types()

    cls.__setstate__ = setstate  # type:ignore


@typechecked
def _override_post_init_method(cls: type):
    old_post_init = getattr(cls, "__post_init__", None)

    # Post init will catch type errors passed when using the generated constructor
    def postinit(self):
        self._validate_member_types()
        if old_post_init is not None:
            old_post_init(self)

    cls.__post_init__ = postinit  # type:ignore


@typechecked
def _override_set_attr_method(cls: type):
    old_set_attr = getattr(cls, "__setattr__", None)

    MISSING = object()

    def setattr(self, name, value):
        # Don't type check private members
        if not name.startswith("_"):
            member_type_map = getattr(cls, "__annotations__", None)
            found_member = False
            if member_type_map is not None:
                expected_type = member_type_map.get(name, MISSING)
                if expected_type is not MISSING:
                    found_member = True
                    typeguard.check_type(name, value, expected_type)
            if not found_member:
                raise AttributeError(
                    f"Type '{self.__class__}' has not declared a member with name '{name}'"
                )

        if old_set_attr is not None:
            old_set_attr(self, name, value)
        else:
            self.__dict__[name] = value

    cls.__setattr__ = setattr  # type:ignore


def _dataclass_typechecked(cls, *args, **kwargs):
    assert not is_dataclass(
        cls
    ), "Not necessary to apply both @dataclass and @dataclass_typechecked"
    cls = dataclass(cls, *args, **kwargs)

    _add_validate_member_types_method(cls)
    _override_set_state_method(cls)
    _override_post_init_method(cls)

    # Setting frozen to True already does this for us and throws if we try and override it
    if not kwargs.get("frozen", False):
        _override_set_attr_method(cls)

    return cls


def dataclass_typechecked(cls=None, *args, **kwargs):
    def wrap(cls):
        return _dataclass_typechecked(cls, *args, **kwargs)

    # See if we're being called as @dataclass_typechecked or @dataclass_typechecked().
    if cls is None:
        # We're called with parameters
        return wrap

    # We're called as @dataclass_typechecked without parameters
    return wrap(cls)
