# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Type

from assemble_workflow.dist import Dist, DistRpm, DistTar, DistZip
from manifests.build_manifest import BuildManifest


class Distribution:

    def __init__(self, cls: Type[Dist], extension: str) -> None:
        self.cls = cls
        self.extension = extension


class Dists:

    DISTRIBUTIONS_MAP = {
        "tar": Distribution(cls=DistTar, extension=".tar.gz"),
        "zip": Distribution(cls=DistZip, extension=".zip"),
        "rpm": Distribution(cls=DistRpm, extension=".rpm"),
    }

    @classmethod
    def create_dist(cls, name: str, path: str, min_path: str, build_cls: BuildManifest.Build) -> Dist:
        distribution = build_cls.distribution or 'tar'
        dist_cls = cls.DISTRIBUTIONS_MAP[distribution].cls

        return dist_cls(name, path, min_path, build_cls)
