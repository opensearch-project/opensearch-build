# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import re

from ci_workflow.ci_input_manifest import CiInputManifest
from ci_workflow.ci_test_manifest import CiTestManifest


class CiManifests:
    def __klass(filename):
        if re.search("-test.yml$", filename):
            return CiTestManifest
        else:
            return CiInputManifest

    @classmethod
    def from_file(cls, file, args):
        return cls.__klass(file.name)(file, args)
