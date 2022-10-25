# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Any, List

from jproperties import Properties


class PropertiesFile(Properties):
    class CheckError(Exception):
        pass

    class UnexpectedKeyValueError(CheckError):
        def __init__(self, key: str, expected: str, current: str = None) -> None:
            super().__init__(
                f"Expected to have {key}='{expected}', but was '{current}'." if current else f"Expected to have {key}='{expected}', but none was found."
            )

    class UnexpectedKeyValuesError(CheckError):
        def __init__(self, key: str, expected: List[str], current: str = None) -> None:
            super().__init__(
                f"Expected to have {key}=any of {expected}, but was '{current}'."
                if current
                else f"Expected to have {key}=any of {expected}, but none was found."
            )

    def __init__(self, data: Any = None) -> None:
        super().__init__(self)
        if type(data) is str:
            self.load(data)
        elif type(data) is dict:
            self.properties = data
        elif data is not None:
            raise TypeError()

    def get_value(self, key: str, default_value: str = None) -> Any:
        try:
            return self[key].data
        except KeyError:
            return default_value

    def check_value(self, key: str, expected: str) -> None:
        try:
            value = self[key].data
            if value != expected:
                raise PropertiesFile.UnexpectedKeyValueError(key, expected, value)
        except KeyError:
            raise PropertiesFile.UnexpectedKeyValueError(key, expected)

    def check_value_in(self, key: str, expected: List[str]) -> None:
        try:
            value = self[key].data
            if value not in expected:
                raise PropertiesFile.UnexpectedKeyValuesError(key, expected, value)
        except KeyError:
            if None not in expected:
                raise PropertiesFile.UnexpectedKeyValuesError(key, expected)
