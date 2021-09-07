# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from system.properties_file import PropertiesFile


class TestPropertiesFile(unittest.TestCase):
    def test_blank(self):
        f = PropertiesFile("")
        self.assertEqual(f.properties, {})

    def test_get_value(self):
        f = PropertiesFile("key: value")
        self.assertEqual(f.get_value("key"), "value")
        self.assertEqual(f.get_value("invalid"), None)
        self.assertEqual(f.get_value("invalid", "default"), "default")

    def test_check_value(self):
        f = PropertiesFile("key: value")
        f.check_value("key", "value")
        with self.assertRaises(
            PropertiesFile.UnexpectedKeyValueError,
            msg="Expected to have key='invalid', but was 'value'.",
        ):
            f.check_value("key", "invalid")
        with self.assertRaises(
            PropertiesFile.UnexpectedKeyValueError,
            msg="Expected to have invalid='value', but none was 'found'.",
        ):
            f.check_value("invalid", "value")

    def test_check_value_in(self):
        f = PropertiesFile("key: value")
        f.check_value_in("key", ["value"])
        with self.assertRaises(
            PropertiesFile.UnexpectedKeyValuesError,
            msg="Expected to have key=any of ['one', 'two'], but was 'value'.",
        ):
            f.check_value_in("key", ["one", "two"])
        with self.assertRaises(
            PropertiesFile.UnexpectedKeyValuesError,
            msg="Expected to have invalid=any of ['one', 'two'], but none was found.",
        ):
            f.check_value_in("invalid", ["one", "two"])
