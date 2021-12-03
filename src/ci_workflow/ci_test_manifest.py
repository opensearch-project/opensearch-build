# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import logging

from ci_workflow.ci_manifest import CiManifest
from manifests.test_manifest import TestManifest


class CiTestManifest(CiManifest):
    def __init__(self, file):
        self.file = file

    def __from_file(self):
        self.manifest = TestManifest.from_file(self.file)

    def check(self):
        try:
            self.__from_file()
            logging.info("TestManifest schema validation succeeded")
            logging.info("Done.")
        except:
            logging.error(f"TestManifest check failed for {self.file.name}")
            raise
