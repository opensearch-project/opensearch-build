# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from system.properties_file import PropertiesFile


class TestPropertiesFile(unittest.TestCase):
    def test_blank(self) -> None:
        f = PropertiesFile()
        self.assertEqual(f.properties, {})

    def test_get_value(self) -> None:
        f = PropertiesFile({"key": "value"})
        self.assertEqual(f.get_value("key"), "value")
        self.assertEqual(f.get_value("invalid"), None)
        self.assertEqual(f.get_value("invalid", "default"), "default")

    def test_check_value(self) -> None:
        f = PropertiesFile({"key": "value"})
        f.check_value("key", "value")

    def test_check_value_invalid(self) -> None:
        f = PropertiesFile({"key": "value"})
        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            f.check_value("key", "invalid")
        self.assertEqual(str(err.exception), "Expected to have key='invalid', but was 'value'.")

    def test_check_value_none_found(self) -> None:
        f = PropertiesFile()
        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            f.check_value("invalid", "value")
        self.assertEqual(str(err.exception), "Expected to have invalid='value', but none was found.")

    def test_check_value_in(self) -> None:
        f = PropertiesFile({"key": "value"})
        f.check_value_in("key", ["value"])

    def test_check_value_in_invalid(self) -> None:
        f = PropertiesFile({"key": "value"})
        with self.assertRaises(PropertiesFile.UnexpectedKeyValuesError) as err:
            f.check_value_in("key", ["one", "two"])
        self.assertEqual(
            str(err.exception),
            "Expected to have key=any of ['one', 'two'], but was 'value'.",
        )

    def test_check_value_in_none_found(self) -> None:
        f = PropertiesFile()
        with self.assertRaises(PropertiesFile.UnexpectedKeyValuesError) as err:
            f.check_value_in("invalid", ["one", "two"])
        self.assertEqual(
            str(err.exception),
            "Expected to have invalid=any of ['one', 'two'], but none was found.",
        )
