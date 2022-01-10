# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from assemble_workflow.dist import Dist, DistZip, DistTar, DistRpm

class Dists:
    DISTRIBUTIONS = {
        "rpm": DistRpm,
        "tar": DistTar,
        "zip": DistZip,
    }  

    @classmethod
    def create_dist(cls, name: str, path: str, distribution: str) -> Dist:
        if distribution not in cls.DISTRIBUTIONS:
            raise ValueError("Distribution not specified or invalid distribution")
        else:
            return cls.DISTRIBUTIONS[distribution](name, path)        
