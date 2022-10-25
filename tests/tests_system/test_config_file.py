# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from system.config_file import ConfigFile


class TestConfigFile(unittest.TestCase):
    def test_blank(self) -> None:
        f = ConfigFile()
        self.assertEqual(f.data, {})

    def test_get_value(self) -> None:
        f = ConfigFile({"key": "value"})
        self.assertEqual(f.get_value("key"), "value")
        self.assertEqual(f.get_value("invalid"), None)
        self.assertEqual(f.get_value("invalid", "default"), "default")

    def test_check_value(self) -> None:
        f = ConfigFile({"key": "value"})
        f.check_value("key", "value")

    def test_check_value_from_json(self) -> None:
        f = ConfigFile('{"key":"value"}')
        f.check_value("key", "value")

    def test_check_value_invalid(self) -> None:
        f = ConfigFile({"key": "value"})
        with self.assertRaises(ConfigFile.UnexpectedKeyValueError) as err:
            f.check_value("key", "invalid")
        self.assertEqual(str(err.exception), "Expected to have key='invalid', but was 'value'.")

    def test_check_value_none_found(self) -> None:
        f = ConfigFile()
        with self.assertRaises(ConfigFile.UnexpectedKeyValueError) as err:
            f.check_value("invalid", "value")
        self.assertEqual(str(err.exception), "Expected to have invalid='value', but none was found.")

    def test_check_value_in(self) -> None:
        f = ConfigFile({"key": "value"})
        f.check_value_in("key", ["value"])

    def test_check_value_in_invalid(self) -> None:
        f = ConfigFile({"key": "value"})
        with self.assertRaises(ConfigFile.UnexpectedKeyValuesError) as err:
            f.check_value_in("key", ["one", "two"])
        self.assertEqual(
            str(err.exception),
            "Expected to have key=any of ['one', 'two'], but was 'value'.",
        )

    def test_check_value_in_none_found(self) -> None:
        f = ConfigFile()
        with self.assertRaises(ConfigFile.UnexpectedKeyValuesError) as err:
            f.check_value_in("invalid", ["one", "two"])
        self.assertEqual(
            str(err.exception),
            "Expected to have invalid=any of ['one', 'two'], but none was found.",
        )
