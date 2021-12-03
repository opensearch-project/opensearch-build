# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc


class CiManifest(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def check(self):
        pass
