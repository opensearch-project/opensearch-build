# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
from typing import Type

from assemble_workflow.dist import Dist, DistTar, DistZip


class Distribution:

    def __init__(self, cls: Type[Dist], extension: str) -> None:
        self.cls = cls
        self.extension = extension


class Dists:

    DISTRIBUTIONS_MAP = {
        "tar": Distribution(cls=DistTar, extension=".tar.gz"),
        "zip": Distribution(cls=DistZip, extension=".zip"),
    }

    @classmethod
    def create_dist(cls, name: str, path: str, min_path: str, distribution: str) -> Dist:
        if distribution is None:
            logging.info("Distribution not specified, default to tar")
            distribution = 'tar'

        dist_cls = cls.DISTRIBUTIONS_MAP[distribution].cls

        return dist_cls(name, path, min_path)
