# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from ci_workflow.ci_check_list_dist import CiCheckListDist
from ci_workflow.ci_check_list_source import CiCheckListSource
from ci_workflow.ci_check_list_source_ref import CiCheckListSourceRef
from ci_workflow.ci_check_lists import CiCheckLists
from manifests.input_manifest import InputComponentFromDist, InputComponentFromSource


class TestCiCheckLists(unittest.TestCase):
    def test_from_component_source(self) -> None:
        check_list = CiCheckLists.from_component(InputComponentFromSource({"name": "common-utils", "repository": "url", "ref": "ref"}), None)
        self.assertIs(type(check_list), CiCheckListSourceRef)

    def test_from_component_source_with_checks(self) -> None:
        check_list = CiCheckLists.from_component(
            InputComponentFromSource({"name": "common-utils", "repository": "url", "ref": "ref", "checks": ["check1"]}), None
        )
        self.assertIs(type(check_list), CiCheckListSource)

    def test_from_component_dist(self) -> None:
        check_list = CiCheckLists.from_component(InputComponentFromDist({"name": "common-utils", "dist": "url"}), None)
        self.assertIs(type(check_list), CiCheckListDist)

    def test_from_component_invalid(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            CiCheckLists.from_component(self, None)
        self.assertTrue(str(ctx.exception).startswith("Invalid component type: "))
