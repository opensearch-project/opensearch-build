# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import json
import os
from typing import Any

from ci_workflow.ci_check import CiCheckSource
from ci_workflow.ci_target import CiTarget
from git.git_repository import GitRepository
from manifests.input_manifest import Component
from system.properties_file import PropertiesFile


class CiCheckPackage(CiCheckSource):
    def __init__(self, component: Component, git_repo: GitRepository, target: CiTarget, args: Any = None) -> None:
        super().__init__(component, git_repo, target, args)
        self.properties = self.__get_properties()

    @property
    def package_json_path(self) -> str:
        return os.path.join(self.git_repo.working_directory, "package.json")

    def __get_properties(self) -> PropertiesFile:
        with open(self.package_json_path, "r") as f:
            return PropertiesFile(CiCheckPackage.__flattenDict(json.load(f)))

    # https://gist.github.com/higarmi/6708779
    @classmethod
    def __flattenDict(cls, d: dict, result: dict = None, index: int = None, parent_key: str = None) -> dict:
        if result is None:
            result = {}
        if isinstance(d, (list, tuple)):
            for indexB, element in enumerate(d):
                if parent_key is not None:
                    newkey = parent_key
                cls.__flattenDict(element, result, index=indexB, parent_key=newkey)
        elif isinstance(d, dict):
            for key in d:
                value = d[key]
                if parent_key is not None and index is not None:
                    newkey = ".".join([parent_key, (str(key).replace(" ", "") + str(index))])
                elif parent_key is not None:
                    newkey = ".".join([parent_key, (str(key).replace(" ", ""))])
                else:
                    newkey = str(key).replace(" ", "")
                cls.__flattenDict(value, result, index=None, parent_key=newkey)
        else:
            result[parent_key] = d
        return result
