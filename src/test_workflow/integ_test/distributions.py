# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from test_workflow.integ_test.distribution import Distribution
from test_workflow.integ_test.distribution_rpm import DistributionRpm
from test_workflow.integ_test.distribution_tar import DistributionTar
from test_workflow.integ_test.distribution_zip import DistributionZip


class Distributions:
    DISTRIBUTIONS_MAP = {
        "tar": DistributionTar,
        "rpm": DistributionRpm,
        "zip": DistributionZip,
    }

    @classmethod
    def from_name(cls, name: str) -> Distribution:
        klass = cls.DISTRIBUTIONS_MAP.get(name, None)
        if not klass:
            raise ValueError(f"Unsupported distribution: {name}")
        return klass  # type: ignore[return-value]

    @classmethod
    def get_distribution(cls, filename: str, distribution: str, version: str, work_dir: str) -> Distribution:
        klass = cls.from_name(distribution)
        logging.info(f"{filename} distribution: {distribution}")
        return klass(filename, version, work_dir)  # type: ignore[no-any-return, operator]
