# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from test_workflow.integ_test.distributions import Distributions


class TestDistributions(unittest.TestCase):

    def setUp(self) -> None:

        self.distributions = Distributions

    def test_distribution_map(self) -> None:
        self.assertEqual(self.distributions.DISTRIBUTIONS_MAP['tar'].__name__, 'DistributionTar')
        self.assertEqual(self.distributions.DISTRIBUTIONS_MAP['rpm'].__name__, 'DistributionRpm')

    def test_create_dist(self) -> None:
        return_cls_tar = self.distributions.get_distribution("opensearch", "tar", "1.3.0", os.path.join(os.path.dirname(__file__), "data"))
        self.assertEqual(return_cls_tar.__class__.__name__, 'DistributionTar')
        return_cls_rpm = self.distributions.get_distribution("opensearch", "rpm", "1.3.0", os.path.join(os.path.dirname(__file__), "data"))
        self.assertEqual(return_cls_rpm.__class__.__name__, 'DistributionRpm')
