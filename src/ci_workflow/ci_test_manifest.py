# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import logging
from io import TextIOWrapper

from ci_workflow.ci_args import CiArgs
from ci_workflow.ci_manifest import CiManifest
from manifests.test_manifest import TestManifest


class CiTestManifest(CiManifest):
    def __init__(self, file: TextIOWrapper, args: CiArgs) -> None:
        super().__init__(TestManifest.from_file(file), args)

    def __check__(self) -> None:
        assert self.manifest
        logging.info("TestManifest schema validation succeeded")
        logging.info("Done.")
