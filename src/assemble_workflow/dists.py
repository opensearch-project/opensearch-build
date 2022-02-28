# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from assemble_workflow.dist import Dist, DistTar, DistZip


class Dists:
    DISTRIBUTIONS_MAP = {
        "tar": DistTar,
        "zip": DistZip,
    }

    @classmethod
    def create_dist(cls, name: str, path: str, min_path: str, distribution: str) -> Dist:
        if distribution is None:
            logging.info("Distribution not specified, default to tar")
            distribution = 'tar'

        return cls.DISTRIBUTIONS_MAP[distribution](name, path, min_path)
