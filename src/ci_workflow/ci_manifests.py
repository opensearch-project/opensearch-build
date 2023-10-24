# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import re
from collections import Counter
from io import TextIOWrapper
from typing import Type, Union

import yaml

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

    @staticmethod
    def __get_duplicate_component_names(count_component_names: Counter) -> list:
        duplicate_component_names = []
        for component_name, count in count_component_names.items():
            if count > 1:
                duplicate_component_names.append(component_name)
        return duplicate_component_names

    @staticmethod
    def __check_duplicate_component_names(file: TextIOWrapper) -> None:
        yaml_dict = yaml.safe_load(file)
        component_names = []
        for component in yaml_dict['components']:
            component_names.append(component['name'])
        count_component_names = Counter(component_names)

        if set(count_component_names.values()) != set([1]):
            duplicate_component_names = CiManifests.__get_duplicate_component_names(count_component_names)
            duplicate_component_names_string = ', '.join(duplicate_component_names)
            raise ValueError(f"Found {duplicate_component_names_string} as a duplicate component(s) in manifest {file.name}. ")
        file.seek(0)

    @classmethod
    def from_file(cls, file: TextIOWrapper, args: CiArgs) -> Union[CiTestManifest, CiInputManifest]:
        cls.__check_duplicate_component_names(file)
        return cls.__klass(file.name)(file, args)
