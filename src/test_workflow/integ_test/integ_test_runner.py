# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc


class IntegTestRunner(abc.ABC):
    def __init__(self, args, test_manifest):
        self.args = args
        self.test_manifest = test_manifest

    @abc.abstractmethod
    def run(self):
        pass
