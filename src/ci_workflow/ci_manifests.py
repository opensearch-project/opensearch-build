# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import re
from io import TextIOWrapper
from typing import Type, Union

from ci_workflow.ci_args import CiArgs
from ci_workflow.ci_input_manifest import CiInputManifest
from ci_workflow.ci_test_manifest import CiTestManifest


class CiManifests:
    @staticmethod
    def __klass(filename: str) -> Union[Type[CiTestManifest], Type[CiInputManifest]]:
        if re.search("-test.yml$", filename):
            return CiTestManifest
        else:
            return CiInputManifest

    @classmethod
    def from_file(cls, file: TextIOWrapper, args: CiArgs) -> Union[CiTestManifest, CiInputManifest]:
        return cls.__klass(file.name)(file, args)
