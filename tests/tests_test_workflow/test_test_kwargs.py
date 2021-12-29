# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from test_workflow.test_kwargs import TestKwargs


class TestTestKwargs(unittest.TestCase):
    def test(self):
        kwargs = TestKwargs(dest="test", option_strings=[])
        mock_parser = MagicMock()
        namespace = SimpleNamespace()
        values = ["key1=value1", "key2=value2"]

        kwargs.__call__(parser=mock_parser, namespace=namespace, values=values)

        self.assertEqual(
            namespace.__getattribute__("test"),
            {
                'key1': os.path.join(os.getcwd(), 'value1'),
                'key2': os.path.join(os.getcwd(), 'value2')
            }
        )
