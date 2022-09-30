# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock

from ci_workflow.ci_check_package import CiCheckPackage
from ci_workflow.ci_target import CiTarget


class TestCiCheckPackage(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")

    class DummyProperties(CiCheckPackage):
        def check(self) -> None:
            pass

    def test_loads_package_json(self) -> None:
        props = TestCiCheckPackage.DummyProperties(
            component=MagicMock(),
            git_repo=MagicMock(working_directory=self.DATA),
            target=CiTarget(version="1.3.0", name="opensearch-dashboards", qualifier=None, snapshot=False),
        )

        self.assertEqual(props.properties["name"].data, "opensearch-security-dashboards")
        self.assertEqual(props.properties["version"].data, "1.3.0.0")
        self.assertEqual(props.properties["opensearchDashboards.version"].data, "1.3.0")
