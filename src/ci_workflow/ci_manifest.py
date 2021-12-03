# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import logging


class CiManifest(abc.ABC):
    def __init__(self, manifest, args):
        self.manifest = manifest
        self.args = args

    def check(self):
        try:
            self.__check__()
        except:
            logging.error("CI Manifest check failed")
            raise
